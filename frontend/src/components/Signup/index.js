import React from 'react'
import { Container, Form, FormContent, FormH1, FormButton, FormInput, FormLabel, FormWrap, Icon, Text } from './SignupElements'
import { useState, } from 'react'
import { useNavigate } from 'react-router-dom';

const SignUp = () => {
    const navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirm, setConfirm] = useState('');
    const [isValid, setIsValid] = useState(false);

    const checkIfValid = (confirm) => {
      return password == confirm;
    }

    const handleConfirm = (e) => {
      setConfirm(e.target.value)
      if (checkIfValid(e.target.value)) {
        setIsValid(true);
      } else {
        setIsValid(false);
      }
    }

    const handleSubmit = async (e) => {
      e.preventDefault();
      if (!isValid) return;
    
      const newUser = {
        email:email,
        password:password,
      };

      try {
        const response = await fetch('http://localhost:3000/signup', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(newUser),
          });
        
      if (response.ok) {
        const result = await response.body;
        console.log('User added successfully:', result);
        navigate('/signin');
      } else {
        throw new Error('An error occured while signing up.');
      }
      } catch (error) {
        console.error(error);
      }
    };

    return (
        <>
        <Container>
            <FormWrap>
                <Icon to="/">Ball play</Icon>
                <FormContent>
                    <Form onSubmit={handleSubmit}>
                        <FormH1>Sign up for your account</FormH1>
                        <FormLabel htmlFor='for'>Email</FormLabel>
                        <FormInput 
                          placeholder="" 
                          type='email' 
                          value={email} 
                          onChange={(e) => setEmail(e.target.value)} 
                          required 
                        />

                        <FormLabel htmlFor='for'>Password</FormLabel>
                        <FormInput
                          placeholder=""
                          type='password'
                          value={password}
                          onChange={(e) => setPassword(e.target.value)} 
                          required
                        />

                        <FormLabel htmlFor='for'>Confirm Password</FormLabel>
                        <FormInput 
                          placeholder=''
                          type='password'
                          value={confirm}
                          onChange={(e) => handleConfirm(e)} 
                          required 
                        />

                        <FormButton type='submit'>Continue</FormButton>

                        <Text to='/signin'>Already have an account? Sign in</Text>
                    </Form>
                </FormContent>
            </FormWrap>            
        </Container>
        </>
    );
};

export default SignUp;