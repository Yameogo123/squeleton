import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  Image,
} from 'react-native';
import { Ionicons, Feather, MaterialCommunityIcons } from '@expo/vector-icons';
import { style_login } from '@/assets/css/security';
import { router } from 'expo-router';
import { useSession } from '@/hooks/ctx';
import { app_color } from '@/assets/constantes/constante';
import { useWarningToast } from '@/hooks/useToast';


type LoginScreenProps = {
    setAction: (action: string) => void;
};

export default function LoginScreen({ setAction }: LoginScreenProps){

    const { signIn } = useSession();
    //const [email, setEmail] = useState("");
    const [tel, setTel] = useState("");
    const [pwd, setPwd] = useState("");
    const [show, setShow] = useState(true);
    const [loading, setLoading] = useState(false);
    const st = { flex: 1 };
    const img = {uri: "https://cdn-icons-png.flaticon.com/512/4140/4140047.png"}

    async function logMe(){
        setLoading(true);
    
        setLoading(false);
    }
    

    return (
        <KeyboardAvoidingView
            style={st}
            behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        >
            <ScrollView
                contentContainerStyle={style_login.container}
                keyboardShouldPersistTaps="handled"
            >
                <Image
                    source={img} // Replace with your actual logo
                    style={style_login.logo}
                    resizeMode="contain"
                />
                <Text style={style_login.loginText}>Connexion</Text>

                {/* Email Input */}
                <View style={style_login.inputContainer}>
                    <Ionicons name="call" size={20} color="#8f9bb3" style={style_login.icon} />
                    <TextInput
                        placeholder="Téléphone (+226 xx)"
                        placeholderTextColor="#8f9bb3"
                        style={style_login.input}
                        keyboardType="phone-pad"
                        autoCapitalize="none"
                        onChangeText={setTel}
                    />
                </View>
                    

                {/* Password Input */}
                <View style={style_login.inputContainer}>
                    <Feather name="lock" size={20} color="#8f9bb3" style={style_login.icon} />
                    <TextInput
                        placeholder="Mot de passe"
                        placeholderTextColor="#8f9bb3"
                        secureTextEntry= {show}
                        style={style_login.input}
                        onChangeText={setPwd}
                    />
                    <Feather name={!show ? "eye" : "eye-off"} onPress={()=>setShow(!show)} size={20} color="#ccc" style={style_login.eyeIcon} />
                </View>

                <TouchableOpacity style={style_login.forgotPassword}>
                    <Text style={style_login.forgotText}>Mot de passe oublié</Text>
                </TouchableOpacity>

                <TouchableOpacity disabled={loading} style={style_login.signInButton} onPress={async () => await logMe()}>
                    <Text style={style_login.signInText}>Envoyer</Text>
                </TouchableOpacity>

                <View style={style_login.dividerContainer}>
                    <View style={style_login.line} />
                    <Text style={style_login.orText}>Ou</Text>
                    <View style={style_login.line} />
                </View>

                <View style={style_login.socialContainer}>
                    <TouchableOpacity style={style_login.socialButton}>
                        <MaterialCommunityIcons name="gmail" size={50} color={app_color} style={style_login.socialButton} />
                    </TouchableOpacity>
                    <TouchableOpacity style={style_login.socialButton}>
                        <MaterialCommunityIcons name="facebook" size={50} color={app_color} style={style_login.socialButton} />
                    </TouchableOpacity>
                </View> 

                <View style={style_login.signupContainer}>
                    <Text style={style_login.signupText}>Pas de compte ? </Text>
                    <TouchableOpacity onPress={() => setAction('register')}>
                        <Text style={style_login.signupLink}>Créer un</Text>
                    </TouchableOpacity>
                </View>
            </ScrollView>
        </KeyboardAvoidingView>
    );
};



