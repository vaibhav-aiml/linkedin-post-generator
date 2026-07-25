from pathlib import Path

html = Path("frontend/index.html").read_text(encoding="utf-8")

required_ids = [
    'analysisResult', 'authBtn', 'authModal', 'avgLength', 'charCount', 'charProgress',
    'darkModeToggle', 'favoritesList', 'historyList', 'loadingOverlay',
    'loginEmail', 'loginForm', 'loginPassword', 'logoutBtn', 'messageContent',
    'messageContext', 'messageForm', 'messagePurpose', 'messageResult', 'mostUsedTopic',
    'popularType', 'postContent', 'postForm', 'postHashtags', 'postResult', 'postType',
    'postsByTypeChart', 'recipientName', 'registerEmail', 'registerForm',
    'registerPassword', 'tabLoginBtn', 'tabRegisterBtn', 'textToAnalyze', 'timelineChart',
    'topic', 'totalPosts', 'userBadge', 'userEmailText'
]

missing = [id_name for id_name in required_ids if f'id="{id_name}"' not in html]
print("DOM IDs Verification Result:")
if missing:
    print("Missing IDs:", missing)
else:
    print("ALL 39 REQUIRED STATIC DOM IDs ARE PRESENT AND 100% VERIFIED IN INDEX.HTML!")
