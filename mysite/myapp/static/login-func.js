  // Function to check Whether both passwords
            // is same or not.
            function checkPassword(form) {
              password1 = form.psw.value;
              password2 = form.repsw.value;

              // If password not entered
              if (password1 == '')
                  alert ("Please enter Password");
                    
              // If confirm password not entered
              else if (password2 == '')
                  alert ("Please enter confirm password");
                    
              // If Not same return False.    
              else if (password1 != password2) {
                  alert ("\nPassword did not match: Please try again...")
                  return false;
              }

              // If same return True.
              else{
                  return true;
              }
            }