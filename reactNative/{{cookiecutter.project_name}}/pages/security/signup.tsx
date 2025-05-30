import React, { useMemo, useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  Modal,
} from 'react-native';
import { Ionicons, Feather, MaterialCommunityIcons } from '@expo/vector-icons';
import { style_sigin } from '@/assets/css/security';
import AnimatedLottieView from "lottie-react-native";
import { app_color } from '@/assets/constantes/constante';
import { useErrorToast, useSuccessToast, useWarningToast } from '@/hooks/useToast';


//import 'react-country-state-city/dist/react-country-state-city.css';

type ScreenProps = {
    setAction: (action: string) => void;
};

export default function RegisterScreen({ setAction }: ScreenProps) {

    const [nom, setNom] = useState('');
    const [prenom, setPrenom] = useState('');
    const [tel, setTel] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [show, setShow] = useState(true);
    const [show2, setShow2] = useState(true);
    const [confirm, setConfirm] = useState(false);
    //const [timer, setTimer] = useState(60);
    const [respect, setRespect] = useState(false);
    const [identic, setIdentic] = useState(false);
    const [loading, setLoading] = useState(false);
    const st = { flex: 1 };
    const ani = {height: 140, width: 140, marginBottom: 40}

    useMemo(async () => {

    }, []);

    useMemo(()=>{

    }, [])

    function LookModal(){
        return (
            <Modal visible={confirm} transparent animationType="slide" focusable>
                <View>
                    <View>
                        <Text>Aperçu des fichiers</Text>
                        <ScrollView showsVerticalScrollIndicator={false}>
                        
                        </ScrollView>
                        <TouchableOpacity>
                            <Text>
                                Fermer
                            </Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </Modal>
        );
    }

    
    async function saveUser(){
        setLoading(true);
        
        setLoading(false);
    }


    return (
        <KeyboardAvoidingView
            style={st}
            behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        >
            <ScrollView 
                showsVerticalScrollIndicator={false}
                contentContainerStyle={style_sigin.container} keyboardShouldPersistTaps="handled"
            >
                <AnimatedLottieView source={require("../../assets/images/lotties/signup.json")} style={ani} autoPlay loop  />
                

                {/* Nom */}
                <View style={style_sigin.inputContainer}>
                    <Ionicons name="person-outline" size={20} color="#8f9bb3" style={style_sigin.icon} />
                    <TextInput
                        placeholder="Nom de Famille *"
                        placeholderTextColor="#8f9bb3"
                        style={style_sigin.input}
                        onChangeText={setNom}
                    />
                </View>

                {/* Prenom */}
                <View style={style_sigin.inputContainer}>
                    <Ionicons name="person-outline" size={20} color="#8f9bb3" style={style_sigin.icon} />
                    <TextInput
                        placeholder="Prénom(s) *"
                        placeholderTextColor="#8f9bb3"
                        style={style_sigin.input}
                        onChangeText={setPrenom}
                    />
                </View>

                {/* Mobile Number */}
                <View style={style_sigin.inputContainer}>
                    <Ionicons name="call-outline" size={20} color="#8f9bb3" style={style_sigin.icon} />
                    <TextInput
                        placeholder="Numéro de téléphone (+33xx) *"
                        placeholderTextColor="#8f9bb3"
                        style={style_sigin.input}
                        keyboardType="phone-pad"
                        onChangeText={(text)=> {
                            setTel(text); setConfirm(false);
                        }}
                    />
                    {/* {tel && <Feather name="check-circle" onPress={()=> setConfirm(!confirm)} size={20} color={app_color} style={style_sigin.eyeIcon} />} */}
                </View>


                {/* Email */}
                <View style={style_sigin.inputContainer}>
                    <Ionicons name="mail-outline" size={20} color="#8f9bb3" style={style_sigin.icon} />
                    <TextInput
                        placeholder="Adresse email"
                        placeholderTextColor="#8f9bb3"
                        style={style_sigin.input}
                        keyboardType="email-address"
                        autoCapitalize="none"
                        onChangeText={setEmail}
                    />
                </View>

                {/* Password */}
                <View style={style_sigin.inputContainer}>
                    <Feather name="lock" size={20} color="#8f9bb3" style={style_sigin.icon} />
                    <TextInput
                        placeholder="Mot de passe *"
                        placeholderTextColor="#8f9bb3"
                        secureTextEntry= {show}
                        style={style_sigin.input}
                        onChangeText={setPassword}
                    />
                    <Feather name={!show ? "eye" : "eye-off"} onPress={()=>setShow(!show)} size={20} color="#ccc" style={style_sigin.eyeIcon} />
                </View>

                {
                    !respect && 
                    <Text>doit avoir au moins une majuscule, un chiffre, un caractère spécial et de longeur supérieur à 8.</Text>
                    
                }

                <View style={style_sigin.inputContainer}>
                    <Feather name="lock" size={20} color="#8f9bb3" style={style_sigin.icon} />
                    <TextInput
                        placeholder="Confirmer mot de passe *"
                        placeholderTextColor="#8f9bb3"
                        secureTextEntry= {show2}
                        style={style_sigin.input}
                        editable={respect} 
                        onChangeText={setConfirmPassword}
                    />
                    <Feather name={!show2 ? "eye" : "eye-off"} onPress={()=>setShow2(!show2)} size={20} color="#ccc" style={style_sigin.eyeIcon} />
                </View>

                {
                    !identic && 
                    <Text>Attention les mots de passe doivent bien correspondre</Text>
                    
                }

                {/* Terms */}
                {/* <View style={style_sigin.termsContainer}>
                    <Checkbox
                        status={acceptedTerms}
                        onValueChange={setAcceptedTerms}
                    /> 
                    <Text style={style_sigin.termsText}>
                        I accept all the <Text style={style_sigin.bold}>Terms & Conditions</Text>
                    </Text>
                </View> */}

                {/* Sign Up Button */}
                <TouchableOpacity style={style_sigin.signUpButton} disabled={loading}>
                    <Text style={style_sigin.signUpText}>Créer</Text>
                </TouchableOpacity>

                {/* Divider */}
                <View style={style_sigin.dividerContainer}>
                    <View style={style_sigin.line} />
                        <Text style={style_sigin.orText}>Ou</Text>
                    <View style={style_sigin.line} />
                </View>

                {/* Social Sign Up */}
                <View style={style_sigin.socialContainer}>
                    <TouchableOpacity style={style_sigin.socialButton}>
                        <MaterialCommunityIcons name="gmail" size={50} color={app_color} style={style_sigin.socialButton} />
                    </TouchableOpacity>
                    <TouchableOpacity style={style_sigin.socialButton}>
                        <MaterialCommunityIcons name="facebook" size={50} color={app_color} style={style_sigin.socialButton} />
                    </TouchableOpacity>
                </View>

                <LookModal />

                {/* Sign In Link */}
                <View style={style_sigin.switchContainer}>
                    <Text style={style_sigin.switchText}>vous avez un compte ? </Text>
                    <TouchableOpacity onPress={() => setAction('login')}>
                        <Text style={style_sigin.signInLink}>se connecter</Text>
                    </TouchableOpacity>
                </View>
            </ScrollView>
        </KeyboardAvoidingView>
    );
};

