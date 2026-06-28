# قائمة الذاكرة المشتركة لحفظ الرومات المشغولة
locked_channels = set()

def try_lock(channel_id: int) -> bool:
    """تحاول تقفل الروم، إذا مقفول ترجع False، وإذا فاضي تقفله وترجع True"""
    if channel_id in locked_channels:
        return False 
    
    locked_channels.add(channel_id)
    return True 

def unlock_channel(channel_id: int):
    """تفك القفل عن الروم بعد انتهاء اللعبة"""
    locked_channels.discard(channel_id)