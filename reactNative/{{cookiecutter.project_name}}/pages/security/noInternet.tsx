import { style_nointernet } from "@/assets/css/security";
import { View } from "moti";
import { Text } from "react-native";
import AnimatedLottieView from "lottie-react-native";



export default function NoInternet(){

    return (
        <View style={style_nointernet.offlineContainer}>
            <AnimatedLottieView source={require("../../assets/images/lotties/noInternet.json")} style={style_nointernet.lottie} autoPlay loop  />
            <Text style={style_nointernet.offlineText}>Pas de connexion internet. En cours de connection ...</Text>
        </View>
    );
}