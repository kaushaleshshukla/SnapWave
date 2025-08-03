# Import all crud modules and create convenience modules
from app.crud import user

# Create a "user" submodule that contains all user-related functions
class UserCRUD:
    from app.crud.user import (
        get_user_by_email,
        get_user_by_username,
        get_user_by_id,
        get_users,
        create_user,
        update_user,
        authenticate_user,
        generate_password_reset_token,
        verify_password_reset_token,
        reset_password,
        generate_email_verification_token,
        verify_email
    )

# Export the user submodule
user = UserCRUD
