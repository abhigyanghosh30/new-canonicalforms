from launchpadlib.launchpad import Launchpad

launchpad = Launchpad.login_anonymously(
    "forms.canonical.com", "production", None, version="devel"
)


def check_user_in_team(user_email, team_name):
    """
    Check if a user is a member of a specific Launchpad team.
    """
    try:
        person = launchpad.people.getByEmail(email=user_email)
        team = launchpad.people[team_name]
        members = team.members_details
        for member in members:
            if member.member.name == person.name:
                return True
        return False
    except Exception as e:
        print(f"Error checking team membership: {e}")
        return False
