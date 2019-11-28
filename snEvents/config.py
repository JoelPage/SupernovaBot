class Config():
    # Reminders
    m_reminders = []
    # Channels
    m_announcementChannel = "#raid-announcements"
    m_signupChannel = "#raid-signups"
    # Sort Order
    m_isAscendingSort = True
    # Time
    m_utcOffset = 0
    # Signups
    m_reactions = { 
        "✅" : "Yes",
        "❌" : "No",
        "❔" : "Unsure" }
    # Default Daily Thumbnails
    m_thumbnails = [
        "https://i.imgur.com/sBFpHZ5.png", # Monday
        "https://i.imgur.com/06DdvTd.png", # Tuesday
        "https://i.imgur.com/eWgmroj.png", # Wednesday
        "https://i.imgur.com/sHfPSth.png", # Thursday
        "https://i.imgur.com/0lWrvhl.png", # Friday
        "https://i.imgur.com/cahcbdw.png", # Saturday
        "https://i.imgur.com/BwObwND.png" # Sunday
    ]



    def __init__(self):
        pass

