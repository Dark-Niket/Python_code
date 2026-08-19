import React, { useState, useEffect } from 'react';
import { View, Text, Button, TextInput, StyleSheet, FlatList } from 'react-native';
import api from '../services/api';

export default function HomeScreen({ navigation }) {
  const [startDate, setStartDate] = useState('');
  const [orders, setOrders] = useState([]);

  const addCycle = async () => {
    try {
      await api.post('/cycles', { startDate });
      alert('Cycle logged');
      setStartDate('');
    } catch (err) {
      console.error(err);
      alert('Failed to log cycle. Ensure you are logged in and date format is YYYY-MM-DD');
    }
  };

  const loadOrders = async () => {
    try {
      const res = await api.get('/orders');
      setOrders(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => { loadOrders(); }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>ReadyFlow (Prototype)</Text>
      <Text>Log cycle start (YYYY-MM-DD):</Text>
      <TextInput style={styles.input} value={startDate} onChangeText={setStartDate} placeholder="2026-08-19" />
      <Button title="Add Cycle" onPress={addCycle} />
      <View style={{height:12}} />
      <Button title="View Prediction" onPress={() => navigation.navigate('Prediction')} />
      <View style={{height:12}} />
      <Button title="Find Nearby Stores" onPress={() => navigation.navigate('Stores')} />
      <View style={{height:12}} />
      <Text style={{fontWeight:'bold', marginTop:12}}>Recent Orders</Text>
      <FlatList
        data={orders}
        keyExtractor={(o) => o._id}
        renderItem={({item}) => (
          <View style={{ padding:8, borderBottomWidth:1 }}>
            <Text>{item.storeName} — {item.status}</Text>
            <Text>ETA: {item.etaMinutes} min</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex:1, padding:16, gap:12 },
  title: { fontSize:18, fontWeight:'bold', marginBottom:12 },
  input: { borderWidth:1, borderColor:'#ccc', padding:8, marginVertical:8 }
});
