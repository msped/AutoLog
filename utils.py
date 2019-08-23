def votes(user_email, build_votes, vote_option):
    if user_email in build_votes:
        return True
    else:
        return False
        