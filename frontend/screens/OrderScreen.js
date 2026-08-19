import React, { useEffect, useState } from 'react';
import { View, Text, Button, FlatList } from 'react-native';
import api from '../services/api';

export default function OrderScreen({ route, navigation }) {
  const { store } = route.params;
  const storeId = store.place_id;
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState({});

  useEffect(() => {
    (async () => {
      try {
        const res = await api.get(`/orders/store/${storeId}/products`);
        setProducts(res.data);
      } catch (err) {
        console.error(err);
        alert('Failed to load products');
      }
    })();
  }, []);

  const add = (sku) => {
    setCart(prev => ({ ...prev, [sku]: (prev[sku] || 0) + 1 }));
  };

  const placeOrder = async () => {
    const items = Object.entries(cart).map(([sku, qty]) => {
      const p = products.find(x => x.sku === sku);
      return { sku, name: p.name, qty, price: p.price };
    });
    if (items.length === 0) return alert('Add items first');
    try {
      const res = await api.post('/orders', { storeId, storeName: store.name, items });
      alert(`Order placed (ETA ${res.data.etaMinutes} min). Order id: ${res.data._id}`);
      navigation.popToTop();
    } catch (err) {
      console.error(err);
      alert('Failed to place order');
    }
  };

  return (
    <View style={{ padding: 16, flex:1 }}>
      <Text style={{ fontWeight: 'bold', fontSize:16 }}>{store.name}</Text>
      <Text style={{ marginBottom: 8 }}>{store.vicinity || store.formatted_address}</Text>

      <FlatList
        data={products}
        keyExtractor={(i) => i.sku}
        renderItem={({item}) => (
          <View style={{ padding: 8, borderBottomWidth:1 }}>
            <Text style={{ fontWeight:'bold' }}>{item.name}</Text>
            <Text>₹{item.price}</Text>
            <Button title="Add" onPress={() => add(item.sku)} />
          </View>
        )}
      />
      <View style={{height:12}} />
      <Button title="Place Order (Simulated)" onPress={placeOrder} />
    </View>
  );
}
