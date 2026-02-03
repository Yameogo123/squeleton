import { sessionType, UserType } from "@/assets/constantes/types";
import { getUser } from "@/API/controller.user";
import { getSessionInfo } from "@/hooks/useStorageState";
import { useEffect, useMemo, useState } from "react";
import { useNavigation } from "expo-router";
import { generateRandomNumber, isEmpty } from "@/API/controller.utils";
import { useSession } from "./ctx";
import moment from "moment";
import { useErrorToast, useWarningToast } from "./useToast";
import { refreshInfo } from "./useInformations";


export function useMe() {
    const session = getSessionInfo() as sessionType;
    const [user, setUser] = useState<UserType | null>(null);
    const [refresh, setRefresh] = useState(1);
    const now = moment();
    const { signOut } = useSession();
    const uId = session?.userId;
    
    useEffect(() => {
        const fetchUser = async () => {
            const diffInDays = moment(session?.expireAt).diff(now, 'days');

            if (diffInDays < 0) {
                signOut();
                return;
            }
            
            const user = await getUser(uId, session?.token);

            if (user && user !== "inexistant") {
                if (!isEmpty(user)) {
                    if (!user?.ville) {
                        useWarningToast("Veuillez renseigner votre ville dans les paramètres.");
                    }
    
                    if (!user?.pays) { // Fixed: was checking ville twice
                        useWarningToast("Veuillez renseigner votre pays dans les paramètres.");
                    }
                }
                setUser(user);
                await refreshInfo();
            } else {
                // deconnexion
                signOut();
                useErrorToast("Merci de vous reconnecter");
            }
        };

        if (uId && session?.token) {
            fetchUser();
        }
    }, [refresh, session?.userId, session?.token]); // Added proper dependencies

    return [user, setRefresh] as const;
}


export function useToken(){
    const session: sessionType = getSessionInfo();
    return session?.token;
}



export function useRefresh(setRefresh: (value: number) => void): void {
    const navigation = useNavigation();

    useEffect(() => {
        const unsubscribe = navigation.addListener('focus', () => {
            setRefresh(generateRandomNumber());
        });
        return unsubscribe;
    }, [navigation]);
}