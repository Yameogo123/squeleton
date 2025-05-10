import { getSessionInfo } from "@/hooks/useStorageState";
import { useEffect, useMemo, useState } from "react";
import { useNavigation } from "expo-router";
import { generateRandomNumber } from "@/API/controller.utils";



export function useMe() {
    // const session = getSessionInfo();
    // const [user, setUser] = useState({});
    // const [refresh, setRefresh] = useState(1);

    // useMemo(
    //     async()=>{
    //         const user = await getUser(session?.userId || '', session?.token);
    //         setUser(user);
    //     }, [session, refresh]
    // )

    // return [user, setRefresh] as [UserType | null, () => void]
}


export function useToken(){
    // const session: sessionType = getSessionInfo();
    // return session?.token;
}


export function useRefresh(setRefresh: (value: number) => void): void {
    // const navigation = useNavigation();

    // useEffect(() => {
    //     const unsubscribe = navigation.addListener('focus', () => {
    //         setRefresh(generateRandomNumber());
    //     });
    //     return unsubscribe;
    // }, [navigation]);
}