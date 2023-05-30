import sqlite3
from sqlite3 import Error
import datetime
import random

today = datetime.date.today()
today_string = "{0}/{1}/{2}".format(today.day,today.month,today.year)

class challenge:
    def __init__(self,player1,player2):
        self.player1=player1
        self.player2=player2
        challenge.kritiria(self)

        
    def kritiria(self):
        
        #κανει έλεγχο εάν υπάρχουν τα ονόματα στο RANKING
        player1 = self.player1
        player2 = self.player2
        if empty_check(player1) == True:
            return print('Δεν υπάρχει παίκτης στη θέση #'+str(player1))
        elif empty_check(player2) == True:
            return print('Δεν υπάρχει παίκτης στη θέση #'+str(player2))

        
        #Υπολογίζει τον αριθμός θέσεων που προκαλεί. απο 1-9 3θεσεις, απο 9-.. 4θεσεις
        k5=4
        if player1<=9:
            k5=3
        if (player1-player2)>k5:
            return print('Ο παίκτης που προκαλείται είναι πάνω από',k5,'θέσεις πάνω από τον παίκτη που προκαλεί. Η πρόκληση είναι άκυρη.')
        elif (player1-player2)<0:
            return print('Ο παίκτης που προκαλείται είναι κάτω από τον παίκτη που προκαλεί. Η πρόκληση είναι άκυρη.')
        elif player1==player2:
            print('Λάθος καταχώρηση.')
            return exit
        print("Η πρόκληση είναι αποδεκτή.")
        answer=input("Νίκησε ο παίκτης στη θέση #{0} που έκανε την πρόκληση;".format(player1))
        answer=answer.upper()
        while answer not in ('ΝΑΊΝΑΙΟΧΙΌΧΙ'):
            answer = input('''Παρακαλώ απαντήστε με "Ναι" ή "Όχι". Νίκησε ο παίκτης στη θέση #{0} που έκανε την πρόκληση; '''.format(player1))
            answer=answer.upper()
        if answer in ('ΝΑΊΝΑΙ'):
            win(player1, player2)
        if answer in ('ΌΧΙΟΧΙ'):
            print("Καμία αλλαγή στην κατάταξη.")

        
        
def dbconnect(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


#Δημιουργία ΔΒ + Πίνακα
def create_table():
    '''Δημιουργία πίνακα με Position, Name, Surname, Wins, Loses, Control_Date όπου Control_Date τελευταία μέρα που έπαιξε αγώνα, ημέρα ένταξης στο club ή τελευταία φορά που υπέστη decay. Position = Primary key'''
    my_conn = dbconnect('tennis_club.db') #Δημιουργεί ΔΒ
    sql_query = "CREATE TABLE IF NOT EXISTS ranking (Position INTEGER PRIMARY KEY, Name VARCHAR(128), Surname VARCHAR(128), Wins INTEGER, Loses INTEGER, Control_Date TEXT);" 
    c = my_conn.cursor()

    c.execute(sql_query) #Δημιουργία Πίνακα με τη Θέση ως Primary Key
    my_conn.commit()
    my_conn.close()


#Αρχικοποίηση κατάταξης
def initialization(players,today_string=today_string):
    '''Δέχεται λίστα με όνομα και επίθετο χωρισμένα με κενό και την εκχωρεί στον πίνακα'''
    random.shuffle(players)
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()
    for i,player in enumerate(players):
        entry = (i+1, players[i][0], players[i][1], 0, 0, today_string)
        c.execute("INSERT INTO ranking VALUES {0}".format(entry))
    my_conn.commit()
    my_conn.close()
    print('Οι παίκτες καταχωρήθηκαν τυχαία στην κατάταξη.')




#Print όλη την κατάταξη
def print_():
    '''Τυπώνει τα ονόματα όμορφα κι ωραία.'''
    if empty_check(1) == True:
        print('Η κατάταξη δεν περιέχει παίκτες!')
    else:
        my_conn = dbconnect('tennis_club.db')
        c = my_conn.cursor()
        print(("{:<7}  {:<13}   {:<23}  {:<7}  {:<7}".format(
                        'Θέση', 'Όνομα', 'Επίθετο', 'Νίκες', 'Ήττες')))
        print('*' * 64)
        result = c.execute("SELECT * FROM ranking;")
        for rec in result.fetchall():
            print("{:<7}  {:<13}   {:<23}  {:<7}  {:<7}".format(rec[0], rec[1], rec[2], rec[3], rec[4]))
        print('*' * 64)
        my_conn.close()

    
#Εισαγωγή παίκτη στο τέλος της κατάταξης, προεπιλεγμένες τιμές για Wins & Loses = 0, Control_Date σήμερα ως ημέρα ένταξης
def insert_bottom(Name='', Surname='', Wins=0, Loses=0, Control_Date=today_string):
    '''Εισαγωγή παίκτη στο τέλος της κατάταξης. Εισάγετε Όνομα και Επώνυμο. Νίκες και ήττες έχουν προεπιλεγμένες τιμές 0.'''
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    flag = empty_check(1)
    if flag == True: #Αν η πρώτη θέση είναι κενή δε χρειάζεται να ληφθεί το δεδομένο της τελευταίας θέσης
        new_last_place = 1
    else:
        x = c.execute("SELECT Position FROM ranking;")
        y = x.fetchall()
        new_last_place = (y[-1][0] + 1) #Καταχώρηση νέας τελευταίας θέσης
    entry = (new_last_place, Name, Surname, Wins, Loses, today_string) #Πλειάδα στοιχείων παίκτη
    c.execute("INSERT INTO ranking VALUES {0};".format(entry)) #Εκχώρηση παίκτη σε αυτή τη θέση
    print('Ο', Name, Surname, 'τοποθετήθηκε στη θέση #'+str(new_last_place))
    my_conn.commit()
    my_conn.close()


#Εισαγωγή παίκτη σε επιλεγμένη θέση στην κατάταξη, προεπιλεγμένες τιμές για Wins & Loses = 0
def insert_place(Rank, Name='', Surname='', Wins=0, Loses=0, Control_Date=today_string):
    '''Εισαγωγή παίκτη σε συγκεκριμένη θέση λόγω γνωστής αντικειμενικά υψηλότερης απόδοσης. Ο παίκτης που βρισκόταν στη θέση θα μεταφερθεί μία θέση κάτω, όπως κι όλοι οι χαμηλότεροι παίκες.'''

    if empty_check(Rank-1) == True and Rank != 1: #Αν προσπαθεί να βάλει τον παίκτη σε θέση πάνω από την οποία δεν υπάρχει άλλος παίκτης
        print("Δεν υπάρχει άλλος παίκτης πριν τη θέση που προσπαθείτε να καταχωρήσετε τον παίκτη", Name, Surname+".")

    else:
        if empty_check(1)== False: #Αν η λίστα έχει παίκτες
            my_conn = dbconnect('tennis_club.db')
            c = my_conn.cursor()

            x = c.execute("SELECT Position FROM ranking;")
            y = x.fetchall()
            last_place = y[-1][0] #Παίρνει τη τελευταία θέση στην κατάταξη...
            my_conn.close()
            update_positions_down(Rank, last_place) #...για να τεθεί παράμετρος εδώ, που μεταθέτονται όλοι οι παίκτες μία θέση κάτω αφήνοντας τη θέση ενδιαφέροντος κενή

        my_conn = dbconnect('tennis_club.db')
        c = my_conn.cursor()

        info = (Rank, Name, Surname, Wins, Loses, today_string) 
        c.execute("INSERT INTO ranking VALUES {0};".format(info)) #Εισαγωγή στην κατάταξη είτε η λίστα έχει παίκτες, είτε δεν έχει και ο χρήστης διάλεξε θέση 1
        print('Ο παίκτης', Name, Surname, 'τοποθετήθηκε επιτυχώς στη θέση #'+str(Rank), 'με', Wins, 'νίκες και', Loses, 'ήττες.')

        my_conn.commit()
        my_conn.close()



#Διαγραφή παίκτη
def delete_player(index):
    '''Διαγράφει τον παίκτη στη θέση που δίνεται από το index και μετακινεί τους κατώτερους παίκτες μία θέση πάνω, καλύπτοντας το κενό που δημιουργείται'''
    if empty_check(index) == True: #Έλεγχος αν η θέση περιέχει άτομο
        print("Δεν υπάρχει παίκτης στη θέση που προσπαθείτε να κάνετε διαγραφή.")
    else:
        my_conn = dbconnect('tennis_club.db')
        c = my_conn.cursor()
        
        c.execute("DELETE FROM ranking WHERE Position={0};".format(index)) #Διαγραφή παίκτη
        c.execute("UPDATE ranking SET Position = Position - 1 WHERE Position > {0};".format(index)) #Ανανέωση λίστας
        
        my_conn.commit()
        my_conn.close()

        print('Ο παίκτης στη θέση #'+str(index), 'διαγράφηκε επιτυχώς.')



#Καταγραφή νίκης με παραμέτρους τις θέσεις τους ΠΡΙΝ την αλλαγή κατάταξης
def win(winner_index, loser_index):
    '''Εισάγετε την έως τώρα θέση νικητή και μετά ηττημένου. Ο νικητής θα λάβει τη θέση του ηττημένου. Ο ηττημένος και όλοι οι παίκτες μεταξύ των δύο θέσεων θα μετακινηθούν μία θέση κάτω.'''
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    c.execute("UPDATE ranking SET Wins = Wins + 1 WHERE Position={0};".format(winner_index)) # + 1 Wins σε νικητή
    c.execute("UPDATE ranking SET Control_Date = '{0}' WHERE Position={1};".format(today_string,winner_index)) #Ανανέωση Control_Date ως ημέρα παιχνιδιού
    c.execute("UPDATE ranking SET Loses = Loses + 1 WHERE Position={0};".format(loser_index)) # + 1 Loses σε ηττημένο
    c.execute("UPDATE ranking SET Control_Date = '{0}' WHERE Position={1};".format(today_string,loser_index))
    sql_query = "SELECT * FROM Ranking WHERE Position={0};".format(winner_index)  #Προσωρινή αποθήκευση νικητή
    x = c.execute(sql_query)

    y = x.fetchall() #Επιστρέφει λίστα, με το y[0] να είναι πλειάδα στοιχείων του νικητή
    c.execute("DELETE FROM ranking WHERE Position={0};".format(winner_index)) #Διαγραφή νικητή από προηγούμενη θέση

    entry = (loser_index, y[0][1], y[0][2], y[0][3], y[0][4], y[0][5]) #Νέα πλειάδα για αλλαγή "Position"
    my_conn.commit()
    my_conn.close()

    update_positions_down(loser_index, winner_index) #Κλήση συνάρτησης ανακατάταξης που κατεβάζει τους παίκτες κατά μία θέση από την winner_index μέχρι ΚΑΙ τη loser_index

    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    c.execute("INSERT INTO ranking(Position, Name, Surname, Wins, Loses, Control_Date) VALUES {0};".format(entry)) #Εισαγωγή νικητή στη θέση ηττημένου

    my_conn.commit()
    my_conn.close()
    print('Το παιχνίδι καταγράφηκε επιτυχώς και η κατάταξη ανανεώθηκε!')


#Μεταθέτει όλα τα Positions κατά ένα κάτω αρχίζοντας από το big_num --> big_num+1 μέχρι ΚΑΙ το small_num-->small_num+1
def update_positions_down(small_num, big_num):
    '''Μετακινεί όλες τις Positions κατά μία κάτω αρχίζοντας από το big_num. Προεπιλογή big_num (αν δεν υπάρχει κενό) πρέπει να είναι η τελευταία θέση. Το small_num θα είναι το Position που θα είναι κενό μετά την κλήση.'''
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    counter = big_num + 1 #Μετρητής τιμής Position που θέλουμε να θέσουμε
    for p in range(big_num, small_num-1, -1): #Πρώτα το big_num γίνεται big_num+1 για να μην έχουμε σύγκρουση Primal Keys
            c.execute('UPDATE ranking SET Position = {0} WHERE Position={1}'.format(counter, p)) #Το p είναι μετρητής τρέχουσας θέσης για το WHERE και μειώνεται σε κάθε loop
            counter = counter - 1 #Μείωση counter για σωστή εισαγωγή Position

    my_conn.commit()
    my_conn.close()



#Μεταθέτει τον παίκτη που υπόκειται σε decay λόγω αδράνειας μία θέση κάτω ανεβάζοντας τον κάτω στη θέση του
def rank_decay(index,today_string=today_string):
    '''Ο παίκτης της θέσης index πέφτει μία θέση λόγω αδράνειας κι ο κάτω του ανεβαίνει στη θέση του.'''
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    x = c.execute("SELECT Position FROM ranking;")
    y = x.fetchall()
    last_place = y[-1][0] #λήψη τελευταίας θέσης
    #Η Control Date ανανεώνεται ως τελευταία ημέρα τροποποίησης ώστε να μην υπόκειται σε decay ξανά πχ αύριο
    x = c.execute("SELECT * FROM ranking WHERE Position={0};".format(index))
    inactive_player = x.fetchall() #Αποθήκευση στοιχείων του παίκτη που υπόκειται σε rank decay
    if last_place == inactive_player[0][0]: #Έλεγχος για την περίπτωση που ο παίκτης είναι τελευταίος
        print("Ο παικτης {0} {1} είναι ήδη στην τελευταία θέση και δεν πέφτει περαιτέρω.".format(inactive_player[0][1], inactive_player[0][2]))
        c.execute("UPDATE ranking SET Control_Date='{0}' WHERE Position={1};".format(today_string, index))
        
    if last_place != inactive_player[0][0]:
        c.execute("DELETE FROM ranking WHERE Position={0};".format(index)) #Διαγραφή του παίκτη
        c.execute("UPDATE ranking SET Position = {0} WHERE Position={1};".format(index,index+1)) #Μετακίνηση του κάτω παίκτη στην πλέον κενή θέση
        entry = (inactive_player[0][0]+1, inactive_player[0][1], inactive_player[0][2], inactive_player[0][3], inactive_player[0][4], today_string)
        c.execute("INSERT INTO ranking VALUES {0};".format(entry)) #Εισαγωγή decaying παίκτη στην πλέον κενή θέση του από κάτω παικτή

    my_conn.commit()
    my_conn.close()


#Απαραιτητο για τις υπόλοιπες εσωτερικές λειτουργίες συναρτήσεων
def empty_check(index):
    '''Ελέγχει αν ο πίνακας έχει παίκτη στη θέση που καταχωρείται κι επιστρέφει boolean type variable'''
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()
    fr = c.execute("SELECT Position FROM ranking WHERE Position={0};".format(index))
    empty_check = fr.fetchall()
    if empty_check == []:
        flag = True
    else:
        flag = False
    my_conn.close()
    return flag
    



def check_ranking_for_decay(today=today):
    '''Ελέγχει αν υπάρχουν παίκτες που υπόκεινται σε decay στην κατάταξη'''
    conn = dbconnect('tennis_club.db')
    cursor = conn.cursor()

    decaylist = [] #Λίστα με παίκτες που θα υποστούν decay
    y = cursor.execute("SELECT Position FROM ranking;")
    ranking = y.fetchall()
    for index in range(1,ranking[-1][0]+1): #reset to timer kathe fora pou vriskei elegxomeno kai ksana apo thn arxh olo ton pinaka = lunetai provlhma antistrofhs listas + 30 hmerwn elegxou h drasthriothtas
        x = cursor.execute("SELECT Control_Date FROM ranking WHERE Position={0}".format(index))
        date = x.fetchall()
        x = date[0][0].split(sep='/') #Διαχωρίζει το string
        last_play_date = datetime.date(int(x[2]),int(x[1]),int(x[0])) #Μετατροπή του tring σε datetime object
        days_since_last_play = (today - last_play_date).days
        if days_since_last_play > 30:
            decaylist.append(index) #Προστίθεται στη λίστα, η αλλαγή δεν γίνεται εδώ γιατί οδηγεί σε logical error του περάσματος for
    conn.commit()
    conn.close()
    
    
    if len(decaylist) != 0: #Αν η λίστα δεν είναι κενή
        
        print('Οι παίκτες '+str(decaylist), 'έπεσαν μία θέση λόγω αδράνειας και η κατάταξη ανανεώθηκε.')
        for i in decaylist[::-1]: #Αντίστροφο πέρασμα της λίστας για αποφυγή λαθών από την αλλαγή θέσης
            rank_decay(i)
            
    
    else:
        print("Δεν υπάρχει κανένας παίκτης που να υπόκειται σε μείωση θέσης λόγω αδράνειας.")



#Main Menu
while True:
    create_table()
    print("-" * 20)
    print("1. Αρχικοποίηση κατάταξης")
    print("2. Προσθήκη παίκτη")
    print("3. Αφαίρεση παίκτη")
    print("4. Έλεγχος και καταγραφή αποτελέσματος πρόκλησης")
    print("5. Έλεγχος κατάταξης για αδρανείς παίκτες")
    print("6. Εμφάνιση κατάταξης")
    print("7. Έξοδος")
    print("-" * 20)
    try:

        choice = int(input("Δώστε την επιλογή σας: "))
        if choice == 1:
            flag = empty_check(1) 
            if flag == False: #Έλεγχος για το αν ο πίνακας περιέχει παίκτες
                print('Ο πίνακας κατάταξης περιέχει ήδη παίκτες και δεν μπορεί να αρχικοποιηθεί τυχαία. Παρακαλώ, διαγράψτε όλους τους παίκτες ή προσθέστε παίκτες χρησιμοποιώντας κάποια από τις επιλογές.')
                continue;
            players = []
            x = ''
            while x != '0':
                x = input("Δώστε όνομα και επίθετο παίκτη που θέλετε να εισάγετε ή 0 για τερματισμό: ")
                player = x.split(sep=' ')
                if x == '0':
                    break;
                if len(player) != 2: #Περίπτωση που εισαχθούν πάνω απο 2 κενά
                    print("Παρακαλώ εισάγετε όνομα και επίθετο χωρισμένα με ένα κενό.")
                    continue
                players.append(x.split(sep=' '))
            if players != []:
                initialization(players) 
            else: #Αν η λίστα players είναι κενή
                print("Δε δημιουργήθηκε κατάταξη καθώς δεν εισάγατε ονόματα.")



        elif choice == 2:
            answer = input("Θέλετε να εισάγετε τον παίκτη σε συγκεκριμένη θέση; ")
            answer=answer.upper()
            while answer not in ('ΝΑΊΝΑΙΟΧΙΌΧΙ'):
                answer = input("Παρακαλώ απαντήστε με Ναι ή Όχι. Θέλετε να εισάγετε τον παίκτη σε συγκεκριμένη θέση; ")
                answer=answer.upper()
                
            while True:
                x = input("Δώστε όνομα και επίθετο παίκτη που θέλετε να εισάγετε: ")
                player = x.split(sep=' ')
                if len(player) != 2: #Περίπτωση που εισαχθούν πάνω απο 2 κενά
                    print("Παρακαλώ εισάγετε όνομα και επίθετο χωρισμένα με ένα κενό.")
                    continue
                break
            name = player[0]
            surname = player[1]
            answer=answer.upper()
            if answer in ('ΝΑΊΝΑΙ'):
                try:
                    rank = (int(input("Δώστε τη θέση κατάταξης του παίκτη που θέλετε να προσθέσετε: ")))
                    insert_place(int(rank),name,surname)
                except ValueError:
                    print("Παρακαλώ, εισάγετε ακέραιο αριθμό για τη θέση κατάταξης.")
            if answer in ('ΌΧΙΟΧΙ'):
                insert_bottom(name,surname)



        elif choice == 3:
            try:
                index = int(input("Δώστε τη θέση κατάταξης του παίκτη που θέλετε να αφαιρέσετε: "))
                delete_player(index)
            except ValueError:
                print("Παρακαλώ, εισάγετε ακέραιο αριθμό για τη θέση κατάταξης.")



        elif choice == 4:
            try:
                p1 = (int(input("Δώστε τη θέση κατάταξης του παίκτη που προκαλεί: ")))
                p2 = (int(input("Δώστε τη θέση κατάταξης του παίκτη που προκαλείται: ")))
            except ValueError:
                print("Παρακαλώ, εισάγετε ακέραιο αριθμό για τη θέση κατάταξης.")
            p = challenge(p1,p2)
            

        
        elif choice == 5:
            check_ranking_for_decay()



        elif choice == 6:
            print_()



        elif choice == 7:
            break;

        
        else:
            print("Λάθος επιλογή. Παρακαλώ επιλέξτε απο το μενού (1-5)")
    except ValueError:
        print("Παρακαλώ εισάγετε μόνο ακεραίους (απο το 1-5)")
