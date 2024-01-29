import React from 'react'
import { Container, Form, FormContent, FormH1, FormButton, FormInput, FormLabel, FormWrap, Icon, Text } from './SignupElements'

const SignUp = () => {
    return (
        <>
        <Container>
            <FormWrap>
                <Icon to="/">Ball play</Icon>
                <FormContent>
                    <Form action="#">
                        <FormH1>Sign up for your account</FormH1>
                        <FormLabel htmlFor='for'>Email</FormLabel>
                        <FormInput type='email' required />
                        <FormLabel htmlFor='for'>Password</FormLabel>
                        <FormInput type='password' required />
                        <FormLabel htmlFor='for'>Confirm Password</FormLabel>
                        <FormInput type='password' required />
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