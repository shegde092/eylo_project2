import firebase_admin
from firebase_admin import credentials, messaging
import logging
from typing import Optional
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class FCMClient:
    """Client for Firebase Cloud Messaging push notifications"""
    
    def __init__(self):
        # Initialize Firebase Admin SDK
        # Note: In production, use a service account JSON file
        # For now, we'll use the server key (legacy method)
        self.server_key = settings.fcm_server_key
        self.initialized = False
    
    def initialize(self, credential_path: Optional[str] = None):
        """Initialize Firebase Admin SDK"""
        if not self.initialized:
            if credential_path:
                cred = credentials.Certificate(credential_path)
                firebase_admin.initialize_app(cred)
            else:
                # Default initialization
                firebase_admin.initialize_app()
            self.initialized = True
    
    async def send_recipe_ready_notification(
        self,
        fcm_token: str,
        recipe_id: str,
        recipe_title: str
    ) -> bool:
        """
        Send push notification that recipe is ready
        
        Args:
            fcm_token: Device FCM token
            recipe_id: UUID of the recipe
            recipe_title: Title to show in notification
            
        Returns:
            True if sent successfully
        """
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title="Recipe Ready! 🍝",
                    body=f"'{recipe_title}' has been imported to your collection"
                ),
                data={
                    "type": "recipe_imported",
                    "recipe_id": str(recipe_id),
                    "deep_link": f"eylo://recipe/{recipe_id}"
                },
                token=fcm_token,
                android=messaging.AndroidConfig(
                    priority="high",
                    notification=messaging.AndroidNotification(
                        icon="ic_recipe",
                        color="#FF6B35",
                        sound="default"
                    )
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            sound="default",
                            badge=1,
                            category="RECIPE_READY"
                        )
                    )
                )
            )
            
            response = messaging.send(message)
            logger.info(f"FCM notification sent: {response}")
            return True
            
        except Exception as e:
            logger.error(f"FCM send failed: {str(e)}")
            return False


# Singleton instance
fcm_client = FCMClient()
