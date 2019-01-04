function validateForm(){
  if(document.myForm.Url.value == "" )
  {
            alert( "Please provide your name!" );
            document.myForm.Url.focus() ;
            return false;
  }
  if(document.myForm.recEmail.value == "" )
  {
            alert( "Please provide your Email!" );
            document.myForm.recEmail.focus() ;
            return false;
  }
  if(document.myForm.mat.value == "" )
  {
            alert( "Please provide your mat!" );
            document.myForm.mat.focus() ;
            return false;
  }
  return true;

}