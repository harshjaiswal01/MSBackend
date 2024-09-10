from database import db
from models.user_details import UserDetails
from models.schemas.user_details_schema import user_details_schema
from services.user_calendar_service import update_user_calendar_on_due_date_change

def get_user_details(user_id):
    """
    Retrieve user details by user ID.
    """
    user_details = db.session.query(UserDetails).filter_by(user_id=user_id).first()
    if not user_details:
        return None, {"error": "User details not found"}
    return user_details_schema.dump(user_details), None

# def create_user_details(user_id, details_data):
#     """
#     Create user details for a user.
#     """
#     user_details = UserDetails(
#         user_id=user_id,
#         sex=details_data['sex'],
#         pronouns=details_data['pronouns'],
#         due_date=details_data.get('due_date'),
#         first_pregnancy=details_data.get('first_pregnancy', False),
#         phone=details_data.get('phone'),
#         can_receive_texts=details_data.get('can_receive_texts', False)
#     )
#     db.session.add(user_details)
#     db.session.commit()

#     # Trigger calendar recalculation
#     update_user_calendar_on_due_date_change(user_id)

#     return user_details_schema.dump(user_details), None

def create_user_details(user_id, details_data):
    try:
        # Extract fields from details_data
        sex = details_data.get('sex')
        pronouns = details_data.get('pronouns')
        due_date = details_data.get('due_date')
        first_pregnancy = details_data.get('first_pregnancy')
        phone = details_data.get('phone')
        can_receive_texts = details_data.get('can_receive_texts')

        # Create the user details object with the associated user_id
        user_details = UserDetails(
            # user_id=user_id,
            sex=sex,
            pronouns=pronouns,
            due_date=due_date,
            first_pregnancy=first_pregnancy,
            phone_number=phone,
            can_receive_text=can_receive_texts
        )

        user_details.user_id = user_id
        # Save the user details to the database
        db.session.add(user_details)
        db.session.commit()

        update_user_calendar_on_due_date_change(user_id)

        return user_details_schema.dump(user_details), None
    except Exception as e:
        return None, {"error": str(e)}

def update_user_details(user_id, details_data):
    """
    Update user details and trigger calendar recalculation if due date changes.
    """
    user_details = db.session.query(UserDetails).filter_by(user_id=user_id).first()

    if not user_details:
        return None, {"error": "User details not found"}

    user_details.sex = details_data.get('sex', user_details.sex)
    user_details.pronouns = details_data.get('pronouns', user_details.pronouns)
    user_details.due_date = details_data.get('due_date', user_details.due_date)
    user_details.first_pregnancy = details_data.get('first_pregnancy', user_details.first_pregnancy)
    user_details.phone_number = details_data.get('phone', user_details.phone_number)
    user_details.can_receive_text = details_data.get('can_receive_texts', user_details.can_receive_text)

    db.session.commit()

    # Trigger recalculation of the user's calendar if due date has changed
    if 'due_date' in details_data:
        update_user_calendar_on_due_date_change(user_id)

    return user_details_schema.dump(user_details), None
