

import random


AVAILABLE_CHARACTERS={}

class Player :

    def __init__(self, name, life, money):
        self.name=name
        self.life=life
        self.team=[]
        self.money=money
        self.game=None
        self.direction=None
        
    
    def __str__(self):
        return "nom joueur : " + self.name + ", vie restante : " + str(self.life) +", personnages en jeu (équipe) : " + str(self.team)+", direction : "+str(self.direction)

    @property
    def is_alive(self):
       return self.life>0

    def check_keys(self,input):
        return input in AVAILABLE_CHARACTERS
    
    def check_lines(self,input):
        line_check=[]
        for i in range(self.game.nb_lines):
            line_check.append(str(i))
        return input in line_check
            

    def get_hit(self,damages):
        """
        Take the damage to life
        """
        self.life=self.life-damages


    def new_character(self):
        """
        Ask to player where add a new Character,
        check if enough monney
        and create the new one
        """

        print('\n')
        print(f"{self.name}, choose the character you're hiring, available choices : ")

        print(" no Character : enter")

        for key,value in AVAILABLE_CHARACTERS.items():
            print("Character :",value.get_name(),"Input :", key)
        print('\n')
        choice=input(f"So,{self.name}, what's your choice  :")

        if choice=="":
            return
        else:
             while not self.check_keys(choice):
                if choice=="":
                    return
                choice=input(f"Wrong input, try again {self.name}  :")
             print(f"U choose",AVAILABLE_CHARACTERS[choice].get_name())


        line = input(f"{self.name}: Wich line would you place the new one (0-{self.game.nb_lines-1}) ?")

        while not self.check_lines(line):
            line = input(f"{self.name}: Wrong input (0-{self.game.nb_lines-1}) ?")
       
        line=int(line)


        if self.money >= AVAILABLE_CHARACTERS[choice].base_price :
            column = 0 if self.direction == +1 else self.game.nb_columns-1
            AVAILABLE_CHARACTERS[choice](self,(line,column))
        else:
            print("no more money")
                    

class Ai(Player):

    def new_character(self):
        """
        Computer's new_character method
        """
        
        ai_choice=random.choice(list(AVAILABLE_CHARACTERS.keys()))
        line=random.randint(0,self.game.nb_lines-1)
        print("Ai choice:",ai_choice)

        if ai_choice!="":
            if self.money >= Character.base_price:
                column = 0 if self.direction == +1 else self.game.nb_columns-1
                AVAILABLE_CHARACTERS[ai_choice](self,(line,column))
            else:
                return("no more money")
        
        else:
            return("No character deployed")




class Game :

    def __init__(self,player0, player1, nb_lines=6,nb_columns=15):

        self.player0=player0
        self.player1=player1
        self.nb_lines=nb_lines
        self.nb_columns=nb_columns
        self.players=[player0,player1]
        self.player_turn=0
        player0.game=self
        player1.game=self
        player0.direction=1
        player1.direction=-1

    def __str__(self):
        return "Game playes by  : " + str(self.player0)+"\n and : " + str(self.player1)

    @property
    def current_player(self):
       return self.players[self.player_turn]

    @property
    def oponent(self):
       if self.player_turn==0:
           return self.player1
       else:
           return self.player0

    @property
    def all_characters(self):
        return self.player0.team+self.player1.team

    def starting_draw(self):

        """
        Draw to choose the starting player
        """

        print("Starting Draw, the closest number from computer choice win \n")

        #entrée utilisateur avec verification
        available_input=[]
        west_test=input(f"{self.player0.name}, enter a number between 1 and 10 :")
         
        for i in range(1,11):
            available_input.append(str(i))

        while west_test not in available_input: 
            west_test=input(f"{self.player0.name},choosen number not between 1 and 10, try again :")

        east_test=input(f"{self.player1.name}, enter a number between 1 and 10 :")

        while east_test==west_test:
            east_test=input(f"{self.player1.name}, choose a different number than {self.player0.name}  :")
        while east_test not in available_input: 
            east_test=input(f"{self.player1.name}, choosen number not between 1 and 10, try again :")

        int_east_test=int(east_test)
        int_west_test=int(west_test)

        #tirage au sort
        lotto=random.randint(1,10)
        print("computer choice",lotto,"\n")

        dif_west=abs(int_west_test-lotto)
        dif_east=abs(int_east_test-lotto)
        
        if dif_west<dif_east:
            self.player_turn=0
            print(self.current_player.name," won !")
        elif dif_east==dif_west:
            print(" ")
            print("****Deuce, choosing starting player randomly****")
            self.player_turn=random.randint(0,1)
            print(self.current_player.name," won !")
        else:
            self.player_turn=1
            print(self.current_player.name," won !")
            



    def get_character_at(self, position:tuple):

        """
        PARAM : - position : tuple
        RETURN : character at the position, None if there is nobody
        """
        i=0
        while i <len(self.all_characters):
            if self.all_characters[i].position==position:
                return self.all_characters[i]
            i=i+1
        return None
           
        

    def place_character(self, character, position:tuple):

        """
        place character to position if possible
        PARAM : - character : Character
                - position : tuple
        RETURN : bool to say if placing is done or not
        """
       
        if self.get_character_at(position)==None and position[0] <=self.nb_lines-1 and 0<=position[1]<=self.nb_columns-1:
            character.position=position
            return True
        else:
            return False


    def draw(self):
    
        """
        print the board

        """
        print(f"{self.players[0].life:<4}{'  '*self.nb_columns}{self.players[1].life:>4}")

        print("----"+self.nb_columns*"--"+"----")

        for line in range(self.nb_lines):
            print(f"|{line:>2}|", end="")
            for col in range(self.nb_columns):
                if self.get_character_at((line,col))==None:
                    print(".", end=" ") #le plateau affiche des point
                else:
                     print(self.get_character_at((line,col)).design, end=" ") #le design des caractere est affiché la ou il y en a sur le plateau
            print(f"|{line:<2}|")

        print("----"+self.nb_columns*"--"+"----")

        print(f"{self.players[0].money:<3}${'  '*self.nb_columns}${self.players[1].money:>3}")


    def play_turn(self):
        """
        play one turn :
            - current player can add a new character
            - current player's character play turn
            - oponent player's character play turn
            - draw the board
        """
        self.current_player.new_character()

        #gestion d'exception car on travaille avec des indices de liste donc il faut gérer le cas ou la liste est vide (plus de joueur en jeu)
        try:
            for i in range(len(self.current_player.team)):
                self.current_player.team[i].play_turn()
        except IndexError:
            return

        try:

            for i in range(len(self.oponent.team)):
                self.oponent.team[i].play_turn()

        except IndexError:
           return

        self.draw()
     


    def play(self):
        print("Let's Play !!! \n ")
        self.starting_draw()
        
        try:
    
            
            while self.player0.is_alive and self.player1.is_alive:
                self.play_turn()
                if self.player_turn==0:
                    self.player_turn=1
                else:
                    self.player_turn=0
            
            if self.player0.is_alive:
                print("\n")
                print(f"Victoire de {self.player0.name} !\n")
    
            else:
                print("\n")
                print(f"Victoire de {self.player1.name} !\n")

        except KeyboardInterrupt:
            if self.player_turn==0:
                print("\n")
                print(f"{self.player0.name} surrenders himself !\n")
            else:   
                print("\n")                                           
                print(f"{self.player1.name} surrenders himself !\n")
                


### PERSONNAGES ###
class Character :
    name="Basic character"
    base_price = 1
    base_life = 5
    base_strength = 1

    def __init__(self, player, position):
       
        self.position=() 
        self.player = player
        self.life = self.base_life
        self.strength = self.base_strength
        self.price = self.base_price

        ok = self.game.place_character(self, position)
        if ok :
            self.player.team.append(self)
            self.player.money -= self.price
        else: 
            print("Impossible deployment")


    @property
    def direction(self):
        return self.player.direction

    @property
    def game(self):
        return self.player.game

    @property
    def enemy(self):
        if self.direction==1:
            return self.game.player1
        else:
            return self.game.player0

    @property
    def design(self):
        
        if self.direction==1:
            return ">"
        elif self.direction==-1:
            return "<"

    @classmethod
    def get_name(cls):
        return cls.name

    def move(self):
     
        if self.direction==1:
            self.game.place_character(self,(self.position[0],self.position[1]+1))
        else:
            self.game.place_character(self,(self.position[0],self.position[1]-1))

        


    def get_hit(self, damages):
        """
        Take the damage to life. If dead, the character is removed from his team and return reward
        PARAM : damages : float
        RETURN : the reward due to hit (half of price if the character is killed, 0 if not)
        """
        self.life-=damages

        if self.life<=0:
            self.player.team.remove(self)
            self.enemy.money+=(self.price)/2
     


    def attack(self):
        """
        Make an attack :
            - if in front of ennemy's base : hit the base
            - if in front of character : hit him (and get reward)
        """
        if self.direction==-1 and self.position[1]==0 :
            self.enemy.get_hit(self.strength)
        
        elif self.direction==1 and self.position[1]==self.game.nb_columns-1 :
            self.enemy.get_hit(self.strength)
        else:
            if self.direction==1:
                front_case_col=self.position[1]+1
            else:
                front_case_col=self.position[1]-1
            
            front_case=(self.position[0],front_case_col)
            

            if self.game.get_character_at(front_case)!=None:
                self.game.get_character_at(front_case).get_hit(self.strength)


    def play_turn(self):

        self.move()
        self.attack()


    def __str__(self):

       return "personnage  " ", vie restante : " + str(self.life) +", force : "+str(self.strength)

AVAILABLE_CHARACTERS["C"]=Character

class Fighter(Character):

    name="Fighter"
    base_price=2
    base_strength=2

    @property
    def design(self):
       if self.direction==1:
            return "F"
       elif self.direction==-1:
            return "f"
    
AVAILABLE_CHARACTERS["F"]=Fighter

class Tank(Character):

    name="Tank"
    base_life=10
    base_price=3

    def __init__(self, player, position):
        self.turn_to_move=True
        super().__init__(player,position)

    
    @property
    def design(self):
       if self.direction==1:
            return "T"
       elif self.direction==-1:
            return "t"
    
    def move(self):
        if self.turn_to_move:
            super().move()
            self.turn_to_move=False
        else:
            self.turn_to_move=True

AVAILABLE_CHARACTERS["T"]=Tank

class Archer(Character):

    name="Archer"
    base_life=1
    base_price=2

    @property
    def design(self):
       if self.direction==1:
            return "A"
       elif self.direction==-1:
            return "a"

    def attack(self):

        if self.direction==-1 and self.position[1]==0 :
            self.enemy.get_hit(self.strength)
        
        elif self.direction==1 and self.position[1]==self.game.nb_columns-1 :
            self.enemy.get_hit(self.strength)
        else:
        
            for i in range(self.game.nb_columns):
                if self.game.get_character_at((self.position[0],i))!=None and self.game.get_character_at((self.position[0],i))!=self:
                    self.game.get_character_at((self.position[0],i)).get_hit(self.strength)
          
    
AVAILABLE_CHARACTERS["A"]=Archer

class Kled(Character):
    
    name="Kled"
    base_price=2
    base_life=2

    def __init__(self, player, position):
        self.armor=0.25
        self.life=self.base_life
        self.mounting_life=1
        super().__init__(player,position)

    @property
    def health(self):
        return self.life+self.mounting_life

    @property
    def design(self):
       if self.direction==1:
           if self.mounting_life>=0:
            return "K̂"
           else:
            return "K"
       elif self.direction==-1:
            if self.mounting_life>=0:
                return "k̂"
            else:
                return "k"   
     

    def move(self):

        if self.mounting_life>0:
            for i in range(2):
                super().move()
        else:
            super().move()



    def get_hit(self, damages):
        if self.mounting_life>0:
            self.mounting_life-=damages*(1-self.armor)
        else:
            self.life-=damages*(1-self.armor)
        
        
        if self.life<=0:
            self.player.team.remove(self)
            self.enemy.money+=(self.price)/2
     

AVAILABLE_CHARACTERS["K"]=Kled



if __name__ == "__main__":

    game_mode=input("Would you like to play against AI ? (yes/no)")
    while game_mode!="yes" and game_mode!="no":
        game_mode=input("Wrong input : (yes/no) ?")

    if game_mode=="yes":
        left_player=Player("West army",20,10)
        right_player=Ai("Computer",20,10)
    else:
        left_player=Player("West army",20,10)
        right_player=Player("East army",20,10)
        
    game=Game(left_player,right_player)
    game.play()

    

  