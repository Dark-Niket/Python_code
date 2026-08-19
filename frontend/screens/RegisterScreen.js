import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert } from 'react-native';
import api from '../services/api';
import { setToken } from '../services/api';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function RegisterScreen({ navigation }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const register = async () => {
    try {
      const res = await api.post('/auth/register', { name, email, password });
      const token = res.data.token;
      await setToken(token);
      await AsyncStorage.setItem('rf_token', token);
      navigation.reset({ index: 0, routes: [{ name: 'Home' }] });
    } catch (err) {
      console.error(err);
      Alert.alert('Register failed', err.response?.data?.message || 'Error');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>ReadyFlow — Register</Text>
      <TextInput style={styles.input} placeholder="name" value={name} onChangeText={setName} />
      <TextInput style={styles.input} placeholder="email" value={email} onChangeText={setEmail} autoCapitalize="none" />
      <TextInput style={styles.input} placeholder="password" secureTextEntry value={password} onChangeText={setPassword} />
      <Button title="Create account" onPress={register} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16, flex:1 },
  title: { fontSize: 18, fontWeight: 'bold', marginBottom: 12 },
  input: { borderWidth:1, borderColor:'#ccc', padding:8, marginBottom:8 }
});
