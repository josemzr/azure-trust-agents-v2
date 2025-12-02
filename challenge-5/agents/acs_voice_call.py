"""
Azure Communication Services Voice Call Module

This module provides functionality to make outbound voice calls using Azure Communication Services
to verify fraudulent transactions with customers.
"""

import os
import json
from typing import Dict, Optional
from azure.communication.callautomation import (
    CallAutomationClient,
    PhoneNumberIdentifier,
    CallInvite,
    RecognizeInputType,
    TextSource,
    CallConnectionProperties,
    DtmfTone
)
from azure.core.messaging import CloudEvent
from dotenv import load_dotenv

load_dotenv(override=True)


class ACSVoiceCallClient:
    """Client for making voice calls via Azure Communication Services"""
    
    def __init__(
        self,
        connection_string: Optional[str] = None,
        source_phone_number: Optional[str] = None,
        cognitive_services_endpoint: Optional[str] = None
    ):
        """
        Initialize the ACS Voice Call Client
        
        Args:
            connection_string: ACS connection string (defaults to env var ACS_CONNECTION_STRING)
            source_phone_number: Source phone number for outbound calls (defaults to env var ACS_PHONE_NUMBER)
            cognitive_services_endpoint: Azure Cognitive Services endpoint for AI features (defaults to env var)
        """
        self.connection_string = connection_string or os.environ.get("ACS_CONNECTION_STRING")
        self.source_phone_number = source_phone_number or os.environ.get("ACS_PHONE_NUMBER")
        self.cognitive_services_endpoint = cognitive_services_endpoint or os.environ.get("ACS_COGNITIVE_SERVICES_ENDPOINT")
        
        if not self.connection_string:
            raise ValueError("ACS_CONNECTION_STRING is required")
        if not self.source_phone_number:
            raise ValueError("ACS_PHONE_NUMBER is required")
        
        self.client = CallAutomationClient.from_connection_string(self.connection_string)
        
    def create_fraud_verification_call(
        self,
        target_phone_number: str,
        customer_name: str,
        transaction_id: str,
        transaction_amount: float,
        currency: str,
        destination_country: str,
        callback_uri: Optional[str] = None
    ) -> Dict:
        """
        Initiate an outbound call to verify a potentially fraudulent transaction
        
        Args:
            target_phone_number: Customer's phone number (E.164 format)
            customer_name: Name of the customer
            transaction_id: Transaction identifier
            transaction_amount: Transaction amount
            currency: Currency code
            destination_country: Destination country code
            callback_uri: Optional callback URI for call events
            
        Returns:
            Dict containing call details including call_id and connection info
        """
        try:
            # Create call invite
            target = PhoneNumberIdentifier(target_phone_number)
            source = PhoneNumberIdentifier(self.source_phone_number)
            
            # Create the fraud alert message
            fraud_alert_message = self._create_fraud_alert_message(
                customer_name=customer_name,
                transaction_id=transaction_id,
                transaction_amount=transaction_amount,
                currency=currency,
                destination_country=destination_country
            )
            
            # Set callback URI (in production, this would be your webhook endpoint)
            # For demo purposes, we'll use a placeholder
            callback_uri = callback_uri or "https://example.com/api/callback"
            
            # Create call with initial message
            call_connection_properties = self.client.create_call(
                target_participant=target,
                source_caller_id_number=source,
                callback_url=callback_uri
            )
            
            return {
                "success": True,
                "call_id": call_connection_properties.call_connection_id,
                "call_connection_properties": {
                    "call_connection_id": call_connection_properties.call_connection_id,
                    "server_call_id": call_connection_properties.server_call_id,
                    "targets": [target_phone_number],
                    "source": self.source_phone_number,
                    "call_connection_state": str(call_connection_properties.call_connection_state),
                },
                "message": fraud_alert_message,
                "target_phone_number": target_phone_number,
                "transaction_id": transaction_id
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "target_phone_number": target_phone_number,
                "transaction_id": transaction_id
            }
    
    def _create_fraud_alert_message(
        self,
        customer_name: str,
        transaction_id: str,
        transaction_amount: float,
        currency: str,
        destination_country: str
    ) -> str:
        """Create a fraud alert message for text-to-speech"""
        return f"""
Hello {customer_name}, this is an urgent security alert from your financial institution.

We have detected a potentially fraudulent transaction on your account.

Transaction Details:
- Transaction ID: {transaction_id}
- Amount: {transaction_amount} {currency}
- Destination: {destination_country}

If you authorized this transaction, please press 1.
If you did NOT authorize this transaction, please press 2.
To speak with a fraud specialist, please press 9.

Your security is our priority. Thank you.
"""
    
    def play_message_and_collect_input(
        self,
        call_connection_id: str,
        message: str,
        max_tones: int = 1,
        timeout_seconds: int = 30
    ) -> Dict:
        """
        Play a message via text-to-speech and collect DTMF input
        
        Args:
            call_connection_id: The call connection ID
            message: Message to play via TTS
            max_tones: Maximum number of DTMF tones to collect
            timeout_seconds: Timeout in seconds for input collection
            
        Returns:
            Dict containing operation details
        """
        try:
            call_connection = self.client.get_call_connection(call_connection_id)
            
            # Create text source for TTS
            play_source = TextSource(text=message)
            
            # Play prompt and recognize input (DTMF)
            # Note: target_participant is automatically inferred from the call participants
            result = call_connection.start_recognizing_media(
                input_type=RecognizeInputType.DTMF,
                play_prompt=play_source,
                interrupt_prompt=True,
                initial_silence_timeout_in_seconds=timeout_seconds,
                operation_context="fraud_verification"
            )
            
            return {
                "success": True,
                "operation": "play_message_and_collect_input",
                "call_connection_id": call_connection_id
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "operation": "play_message_and_collect_input",
                "call_connection_id": call_connection_id
            }
    
    def handle_dtmf_response(self, dtmf_input: str, transaction_id: str) -> Dict:
        """
        Handle customer's DTMF response
        
        Args:
            dtmf_input: DTMF tone(s) received from customer
            transaction_id: Transaction ID being verified
            
        Returns:
            Dict with verification result and recommended action
        """
        verification_result = {
            "transaction_id": transaction_id,
            "customer_response": dtmf_input,
            "timestamp": None  # Would be set in production
        }
        
        if dtmf_input == "1":
            verification_result["verification_status"] = "AUTHORIZED"
            verification_result["recommended_action"] = "ALLOW"
            verification_result["message"] = "Customer confirmed transaction is legitimate"
        elif dtmf_input == "2":
            verification_result["verification_status"] = "FRAUDULENT"
            verification_result["recommended_action"] = "BLOCK"
            verification_result["message"] = "Customer confirmed transaction is fraudulent - BLOCK immediately"
        elif dtmf_input == "9":
            verification_result["verification_status"] = "ESCALATED"
            verification_result["recommended_action"] = "INVESTIGATE"
            verification_result["message"] = "Customer requested to speak with specialist - escalate to fraud team"
        else:
            verification_result["verification_status"] = "NO_RESPONSE"
            verification_result["recommended_action"] = "INVESTIGATE"
            verification_result["message"] = "No valid response received from customer"
        
        return verification_result
    
    def terminate_call(self, call_connection_id: str) -> Dict:
        """
        Terminate an active call
        
        Args:
            call_connection_id: The call connection ID to terminate
            
        Returns:
            Dict containing termination status
        """
        try:
            call_connection = self.client.get_call_connection(call_connection_id)
            call_connection.hang_up(is_for_everyone=True)
            
            return {
                "success": True,
                "operation": "terminate_call",
                "call_connection_id": call_connection_id
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "operation": "terminate_call",
                "call_connection_id": call_connection_id
            }


def create_fraud_verification_call_sync(
    target_phone_number: str,
    customer_name: str,
    transaction_id: str,
    transaction_amount: float,
    currency: str,
    destination_country: str
) -> Dict:
    """
    Synchronous helper function to create a fraud verification call
    
    This is a convenience function for integration with the agent workflow.
    Returns a dict with success/error information for graceful error handling.
    """
    try:
        client = ACSVoiceCallClient()
        return client.create_fraud_verification_call(
            target_phone_number=target_phone_number,
            customer_name=customer_name,
            transaction_id=transaction_id,
            transaction_amount=transaction_amount,
            currency=currency,
            destination_country=destination_country
        )
    except ValueError as e:
        # ACS not configured - return error dict instead of raising
        return {
            "success": False,
            "error": f"ACS configuration error: {str(e)}",
            "target_phone_number": target_phone_number,
            "transaction_id": transaction_id
        }
    except Exception as e:
        # Any other error
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "target_phone_number": target_phone_number,
            "transaction_id": transaction_id
        }
