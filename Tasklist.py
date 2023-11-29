
import sqlite3

class App:

     #create a connection to the sqllite database and make tables
     def  __init__ (self, conn):
       self.conn = conn
       self.create_tables()  #creating an instance of the table method inside the constructor ensures 
                            #that the tables are automatically made everytime an instance of the class is created

     status_categories = ['doing', 'todo', 'done']


     def create_tables (self):
     
       create_todo_table = '''
      
         CREATE TABLE IF NOT EXISTS Tasks (
           id integer primary key AUTOINCREMENT, 
           task TEXT NOT NULL,
           status Text NOT NULL
         
      )

     '''

       self.conn.execute(create_todo_table)
       self.conn.commit()
     

     def Add_task (self, task, status):
          try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO Tasks (task, status) VALUES (?,?)", (task, status))
            self.conn.commit()
          except Exception as e: 
            print(f"Error adding taks: {e}")
            self.conn.rollback()  #goes back to the previous version
          finally:
            cursor.close()

            #in the add method, the add logic simply adds the parameters as values for the table attribute
            #all of the logic is encapsulated inside a try and catch block. 

      #UI Method call (Add_task)

     def AddUI (self, app_instance):
        print("***Add Tasks ***")
        print("-----------------")
        
        while True: 

            user_task = input("Please enter your task (250 chars) : ")
            task_category = input("Please enter the category: ")

            if len(user_task) > 250:
               print("Error: Character limit exceeded")
               return
               
            elif task_category.lower() not in App.status_categories: 
               print("Error: Please enter a valid category")
               return
             
            app_instance.Add_task(user_task, task_category)
            print("task added to the list :)")
        
            break
        
           


    
     def Delete_task (self, id):
         try:
           cursor = self.conn.cursor()
           cursor.execute("DELETE From Tasks Where id = ? ", (id))
           self.conn.commit()
         except Exception as e:
           print(f"Error adding tasks: {e}")
           self.conn.rollback()
         finally:
           cursor.close()


      #UI method call Delete_task

     def DeleteUI (self):
        print("***Deleting tasks***")
        print("--------------------")
        
        while True: 
          user_input = int(input("Please enter the task id: "))
          print(user_input)


          if not user_input.isDigit():
             print("wrong ID, please enter again")
             return
          
          self.Delete_task(user_input)
          break
      

      # Print all the 
      
     def Print_records(self, statuses):
         
    
          
         try: 
             
             cursor = self.conn.cursor()
             query = "SELECT * from Tasks Where status in ({})".format(','.join('?' for _ in statuses))
             cursor.execute(query, statuses)
             rows = cursor.fetchall()
             
             if rows:  #if rows are not empty
                num_columns = 3 #three display coloumns
                for i in range(0, len(rows), num_columns):  
                   for task in rows[i:i + num_columns]:
                      print(f"{task[0]:<5} {task[1]:<30} {task[2]}")
                   print() #separating coloumns with an empty line

                else:
                  print("no tasks found")

         except Exception as e:
             print("no tasks found yet")
         finally:
            cursor.close()

      
      #Search method

     def Search_records(self, task):
        
        try:
           
           cursor = self.conn.cursor()
           query = "Select * from Tasks where task Like ?"
           cursor.execute(query,('%'+ task + '%',))
           rows = cursor.fetchall()

           if rows:
                num_columns = 3
                for i in range(0, len(rows), num_columns):
                    for task in rows[i:i + num_columns]:
                        print(f"{task[0]:<5} {task[1]:<30} {task[2]}")
                    print()
           else:
                print("No matching tasks found.")

        except Exception as e: 
           
           print(f"Error: {e}")

        finally:
           
           cursor.close()
           
     
    #Search UI

     def SearchUI(self):
        
        print("***Searching Tasks****")
        print("----------------------")

        while True: 
          user_input = input("Enter task to find: ")
          print(user_input)

          self.Search_records(user_input)
          return
           

         
        




  

     @staticmethod
     def Main ():
        
        #create a connection to the sqllite database
        conn = sqlite3.connect(r'C:\Users\helle\OneDrive\Documents\Sqllite\sqlite3.db')

      #cursor to handle the database 
        cursor = conn.cursor()

        app_instance = App(conn)

        while True:
         
         print("__Task Manager__")
        
        
         print("1. Add Tasks")
         print("2. Delete Tasks")
         print("3. Search Tasks")
         print("3. Print all tasks")

         choice = int(input("Which would you like to do? : "))
        
         if choice == 1: 
            app_instance.AddUI(app_instance)
            
         elif choice == 2:
            app_instance.DeleteUI()
           
         elif choice == 3:
            app_instance.SearchUI() #replace with search method

         elif choice == 4:
            app_instance.Print_records(['todo', 'doing', 'done'])
            
         elif choice == 4:
            print("Press any key to exit....")
            break
         else:
           return "wrong number selected. please enter the right option"


         conn.close()

         
App.Main()









