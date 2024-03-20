import React from 'react'
import { Container, Form, FormContent, FormH1, FormButton, Text, FormInput, FormLabel, FormWrap, Icon, } from './RecoveryElements'

const Recovery = () => {
    return (
        <>
        <Container>
            <FormWrap>
                <Icon to="/">Ball play</Icon>
                <FormContent>
                    <Form action="#">
                        <FormH1>Recover your password</FormH1>
                        <FormLabel htmlFor='for'>Email</FormLabel>
                        <FormInput type='email' required />
                        <FormButton type='submit'>Send recovery email</FormButton>
                        <Text to='/signin'>Remember password? Sign in</Text>
                    </Form>
                </FormContent>
            </FormWrap>            
        </Container>
        </>
    );
};

export default Recovery;