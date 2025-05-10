
import { useMe, useRefresh } from '@/hooks/useUser';
import React from 'react';
import { View } from 'react-native';

export default function HomeScreen() {

  const [user, setRefresh] = useMe();
  
  useRefresh(setRefresh);
 
  return (
    <View style={{flex: 1}}>
      {/* { 
        user?.role === "MEDECIN" ? <MedecinHome user={user} /> : user && <PatientHome user={user} />
      } */}
    </View>
  );
}

