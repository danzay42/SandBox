class Flashlight:
    _color: str = 'white'
    
    def on(self):
        print(f'''
         ________/ | - - - - - -
        |___ON___| | {self._color} 
                 \_| - - - - - -
              ''')
    
    def off(self):
        print('''
         ________/ |
        |___OFF__| | 
                 \_|
              ''')
    
    def color(self, c: str):
        self._color = c
        print(f'''
         ________/ | - - - - - -
        |___ON___| | {self._color} 
                 \_| - - - - - -
              ''')

