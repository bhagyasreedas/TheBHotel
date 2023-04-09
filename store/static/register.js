

function validate() 
      { 
          
        var abc=document.forms["myForm"]["first_name"].value;
          if(abc=="")
          {
              alert("Please enter the first name");
              return false;
          }
          var def=document.forms["myForm"]["last_name"].value;
          if(def=="")
          {
            alert("Please enter the last name");
            return false;
          }
          var email = document.forms["myForm"]["email"].value;
          var re = "/^[a-z0-9+_.-]+@[a-z0-9.-]+$"
          var x=re.test(email);
          if(x)
          {}
          else
          {
            alert("Email id not in correct format");
            return false;
          }      

          var mobile = document.forms["myForm"]["mobile"].value;        
          var check="^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$"
          var a=check.test(mobile);
          if(a)
          {}
          else
          {
            alert("Invalid mobile number");
          }
        }