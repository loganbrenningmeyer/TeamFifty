import React from 'react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom';
import { Container, Form, FormContent, FormH1, FormButton, Text, FormInput, FormLabel, FormWrap, Icon, Text2 } from './SigninElements'

const SignIn = () => {

    const navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch('http://localhost:3000/signin', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (response.ok) {
                const result = await response.json();
                console.log('User found:', result);
                navigate('/');
            } else {
                throw new Error('An error occurred while signing in.');
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
                    <Form action="#" onSubmit={handleSubmit}>
                        <FormH1>Sign in to your account</FormH1>
                        <FormLabel htmlFor='for'>Email</FormLabel>
                        <FormInput 
                            type='email'
                            value={email} 
                            required
                            onChange={(e) => setEmail(e.target.value)}
                        />

                        <FormLabel htmlFor='for'>Password</FormLabel>
                        <FormInput 
                            type='password' 
                            required
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />

                        <Text2 to='/account-recovery'>Forgot Password?</Text2>
                        <FormButton type='submit'>Continue</FormButton>
                        <Text to='/signup'>New User? Sign up</Text>
                    </Form>
                </FormContent>
            </FormWrap>            
        </Container>
        </>
    );
};

export default SignIn;