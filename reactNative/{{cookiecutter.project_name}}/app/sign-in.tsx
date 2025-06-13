

import React, { useState } from 'react';
import { SafeAreaView } from 'react-native';
import WelcomeScreen from '@/pages/welcome';
import LoginScreen from '@/pages/security/login';
import RegisterScreen from '@/pages/security/signup';
import { StatusBar } from 'expo-status-bar';



export default function SignIn(){

    const [action, setAction] = useState('welcome');
    const st = {flex: 1}
    return (
        <SafeAreaView style={st}>
            {
                action === 'login' ? (
                    <LoginScreen setAction={setAction} />
                ) : (
                    action === 'welcome' ? (
                        <WelcomeScreen setAction={setAction} />
                    ) : (
                        <RegisterScreen setAction={setAction} />
                    )
                )
            }
            <StatusBar style="dark" />
        </SafeAreaView>
    );
};


  