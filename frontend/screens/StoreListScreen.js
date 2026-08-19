import React, { useState } from 'react';
import { View, Text, TextInput, Button, FlatList, TouchableOpacity } from 'react-native';
import api from '../services/api';

export default function StoreListScreen({ navigation }) {
  const [lat, setLat] = useState('');
  const [lng, setLng] = useState('');
  const [stores, setStores] = useState(null);

  const findStores = async () => {
    try {
      const res = await api.get('/stores', { params: { lat, lng, radius: 2000, type: 'pharmacy' } });
      setStores(res.data.results || []);
    } catch (err) {
      console.error(err);
      alert('Failed to fetch stores. Ensure backend has GOOGLE_PLACES_API_KEY configured.');
    }
  };

  return (
    <View style={{ padding: 16, flex:1 }}>
      <Text>Enter your location (lat / lng)</Text>
      <TextInput placeholder="lat" value={lat} onChangeText={setLat} style={{ borderWidth:1, padding:8, marginVertical:6 }} />
      <TextInput placeholder="lng" value={lng} onChangeText={setLng} style={{ borderWidth:1, padding:8, marginVertical:6 }} />
      <Button title="Find nearby pharmacies" onPress={findStores} />
      <View style={{height:12}} />
      {stores && (
        <FlatList
          data={stores}
          keyExtractor={(i) => i.place_id}
          renderItem={({item}) => (
            <TouchableOpacity onPress={() => navigation.navigate('Order', { store: item })} style={{ padding:12, borderBottomWidth:1 }}>
              <Text style={{ fontWeight:'bold' }}>{item.name}</Text>
              <Text>{item.vicinity || item.formatted_address}</Text>
            </TouchableOpacity>
          )}
        />
      )}
    </View>
  );
}
