import React from 'react'
import { Grid } from "@material-ui/core";




function PasswordRegexChecks({password}) {
    const hasLowercase = (str) => {
        return /[a-z]/.test(str);
      };
    
      const hasUppercase = (str) => {
        return /[A-Z]/.test(str);
      };
    
      const hasNumber = (str) => {
        return /[0-9]/.test(str);
      };
    
      const hasSpecialChar = (str) => {
        return /[ `!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/.test(str);
      };
    
      const hasEightChar = (str) => {
        return str.length > 7;
      };
    
      const hasUnderFiftyChar = (str) => {
        return str.length < 50;
      };


    return (
<Grid item xs={12} align="left">
          <Grid container spacing={3}>
            <Grid item xs={6} align="left">
              <input
                type="radio"
                id="hasLowercase"
                checked={hasLowercase(password)}
              />
              <label htmlFor="hasLowercase"> One lowercase character</label>
            </Grid>
            <Grid item xs={6} align="left">
              <input
                type="radio"
                id="hasUppercase"
                checked={hasUppercase(password)}
              />
              <label htmlFor="hasUppercase"> One uppercase character</label>
            </Grid>
            <Grid item xs={6} align="left">
              <input
                type="radio"
                id="hasNumber"
                checked={hasNumber(password)}
              />
              <label htmlFor="hasNumber"> One number</label>
            </Grid>
            <Grid item xs={6} align="left">
              <input
                type="radio"
                id="hasSpecialChar"
                checked={hasSpecialChar(password)}
              />
              <label htmlFor="hasSpecialChar"> One special character</label>
            </Grid>
            <Grid item xs={6} align="left">
              <input
                type="radio"
                id="hasEightChar"
                checked={hasEightChar(password)}
              />
              <label htmlFor="hasEightChar"> 8 characters minimum</label>
            </Grid>
            <Grid item xs={6} align="left">
              <input
                type="radio"
                id="hasUnderFiftyChar"
                checked={hasUnderFiftyChar(password)}
              />
              <label htmlFor="hasUnderFiftyChar"> 50 characters maximum</label>
            </Grid>
          </Grid>
        </Grid>
    )
}


export default PasswordRegexChecks

