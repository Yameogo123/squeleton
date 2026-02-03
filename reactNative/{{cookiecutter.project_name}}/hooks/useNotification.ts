import { useState, useRef } from 'react';
import * as Notifications from 'expo-notifications';
//import { useSession } from './ctx';
import { useFocusEffect } from '@react-navigation/native';
import { updateExpoToken } from '@/API/controller.utils';

Notifications.setNotificationHandler({
    handleNotification: async () => ({
        shouldShowAlert: true,
        shouldPlaySound: true,
        shouldSetBadge: true,
        shouldShowBanner: true,
        shouldShowList: true,
    }),
});


export function useNotification(userId?: string, tok?: string, existant_token:string = '', setRefresh?: any) {
    const [notification, setNotification] = useState<Notifications.Notification | undefined>(undefined);
    const notificationListener = useRef<Notifications.EventSubscription | null>(null);
    const responseListener = useRef<Notifications.EventSubscription | null>(null);

    async function registerForPushNotificationsAsync() {
        const { status: existingStatus } = await Notifications.getPermissionsAsync();
        let finalStatus = existingStatus;

        if (existingStatus !== "granted") {
            const { status } = await Notifications.requestPermissionsAsync();
            finalStatus = status;
        }

        if (finalStatus !== "granted") {
            return null;
        }

        const token = (await Notifications.getExpoPushTokenAsync()).data;
        return token;
    }

    useFocusEffect(() => {
        let isActive = true;

        registerForPushNotificationsAsync()
        .then(expo_token => {
            //updateExpoToken(token, userId, tok); // store token in backend
            if (isActive && expo_token) {
                if(existant_token !== expo_token){
                    updateExpoToken(expo_token, userId, tok); 
                }
            }
        })
        .catch(err => {
            
        });

        notificationListener.current = Notifications.addNotificationReceivedListener(notif => {
            if (isActive) setNotification(notif);
            setRefresh(Math.random()); 
        });

        responseListener.current = Notifications.addNotificationResponseReceivedListener(response => {
            setRefresh(Math.random()); 
        });

        return () => {
            isActive = false;
            notificationListener.current?.remove();
            responseListener.current?.remove();
        };
    });

    return notification;
}