import React, { useEffect, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import AsyncStorage from '@react-native-async-storage/async-storage';
import HomeScreen from './screens/HomeScreen';
import PredictionScreen from './screens/PredictionScreen';
import LoginScreen from './screens/LoginScreen';
import RegisterScreen from './screens/RegisterScreen';
import StoreListScreen from './screens/StoreListScreen';
import OrderScreen from './screens/OrderScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  const [isSignedIn, setIsSignedIn] = useState(null);

  useEffect(() => {
    (async () => {
      const t = await AsyncStorage.getItem('rf_token');
      setIsSignedIn(!!t);
    })();
  }, []);

  if (isSignedIn === null) return null;

  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName={isSignedIn ? "Home" : "Login"}>
        {isSignedIn ? (
          <>
            <Stack.Screen name="Home" component={HomeScreen} />
            <Stack.Screen name="Prediction" component={PredictionScreen} />
            <Stack.Screen name="Stores" component={StoreListScreen} />
            <Stack.Screen name="Order" component={OrderScreen} />
          </>
        ) : (
          <>
            <Stack.Screen name="Login" component={LoginScreen} />
            <Stack.Screen name="Register" component={RegisterScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
