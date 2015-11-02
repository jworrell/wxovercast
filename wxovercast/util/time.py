import datetime

def decode_time_6(time_str):
    now = datetime.datetime.now()
    day, hour, minute = int(time_str[0:2]), int(time_str[2:4]), int(time_str[4:6])
    
    now_guess = datetime.datetime(now.year, now.month, day, hour, minute)
        
    if day == now.day:
        return now_guess
        
    else:
        month = now.month+1
        year = now.year
        if month > 12:
            month = 1
            year += 1
            
        next_guess = datetime.datetime(year, month, day, hour, minute)
        
        month = now.month-1
        year = now.year
        if month < 1:
            month = 12
            year -= 1
        
        last_guess = datetime.datetime(year, month, day, hour, minute)
        
        guesses = [last_guess, now_guess, next_guess]
        
        deltas = [now - last_guess, 
                  now - now_guess if now > now_guess else now_guess - now, 
                  next_guess - now]
        
        return guesses[deltas.index(min(deltas))]
