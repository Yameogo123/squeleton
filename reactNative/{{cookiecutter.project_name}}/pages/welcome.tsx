import React, { useRef, useState } from 'react';
import {
  View, Text, FlatList, Dimensions, TouchableOpacity,
} from 'react-native';

const { width } = Dimensions.get('window');


type WelcomeScreenProps = {
  setAction: (action: string) => void;
};

export default function WelcomeScreen({ setAction }: WelcomeScreenProps) {

  return (
    <View style={{flex: 1}}>
      <TouchableOpacity onPress={() => setAction('login')}>
        <Text>commencer</Text>
      </TouchableOpacity>
    </View>
  );
};


