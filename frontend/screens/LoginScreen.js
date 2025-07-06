import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, TouchableOpacity, Alert, Platform } from 'react-native';
import apiService from '../services/api';

export default function LoginScreen({ navigation }) {
  const [phone, setPhone] = useState('');
  const [agree, setAgree] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleDirectLogin = async () => {
    if (!/^1\d{10}$/.test(phone)) {
      Alert.alert('请输入有效的手机号');
      return;
    }
    if (!agree) {
      Alert.alert('请先同意用户协议和隐私政策');
      return;
    }
    setLoading(true);
    try {
      const response = await apiService.directLogin(phone);
      navigation.replace('Main');
    } catch (error) {
      Alert.alert('登录失败', error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleNext = () => {
    handleDirectLogin();
  };

  return (
    <View style={styles.container}>
      <Text style={styles.logo}>面经快车</Text>
      <Text style={styles.title}>登录/注册</Text>
      <Text style={styles.desc}>首次验证通过即注册面经快车账号</Text>
      <View style={styles.inputRow}>
        <Text style={styles.areaCode}>+86</Text>
        <TextInput
          style={styles.input}
          placeholder="请输入手机号"
          keyboardType="phone-pad"
          maxLength={11}
          value={phone}
          onChangeText={setPhone}
        />
        {phone.length > 0 && (
          <TouchableOpacity onPress={() => setPhone('')}>
            <Text style={styles.clearBtn}>×</Text>
          </TouchableOpacity>
        )}
      </View>
      <TouchableOpacity 
        style={[styles.nextBtn, loading && styles.nextBtnDisabled]} 
        onPress={handleNext}
        disabled={loading}
      >
        <Text style={styles.nextBtnText}>
          {loading ? '登录中...' : '直接登录'}
        </Text>
      </TouchableOpacity>
      <View style={styles.protocolRow}>
        <TouchableOpacity onPress={() => setAgree(!agree)}>
          <Text style={styles.checkbox}>{agree ? '●' : '○'}</Text>
        </TouchableOpacity>
        <Text style={styles.protocolText}>
          已阅读并同意
          <Text style={styles.link}>《面经快车用户协议》</Text>
          和
          <Text style={styles.link}>《隐私政策》</Text>
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', padding: 24 },
  logo: { color: '#00C6AE', fontWeight: 'bold', fontSize: 22, alignSelf: 'center', marginTop: 16, marginBottom: 24 },
  title: { fontSize: 26, fontWeight: 'bold', marginBottom: 8 },
  desc: { color: '#888', marginBottom: 32 },
  inputRow: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#F6F7FB', borderRadius: 8, paddingHorizontal: 12, marginBottom: 16 },
  areaCode: { fontSize: 18, color: '#222', marginRight: 8 },
  input: { flex: 1, fontSize: 18, paddingVertical: 12, backgroundColor: 'transparent' },
  clearBtn: { fontSize: 22, color: '#bbb', padding: 4 },
  nextBtn: { backgroundColor: '#00C6AE', borderRadius: 8, marginTop: 8, marginBottom: 16, height: 48, justifyContent: 'center', alignItems: 'center' },
  nextBtnDisabled: { backgroundColor: '#ccc' },
  nextBtnText: { color: '#fff', fontSize: 20 },
  protocolRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 16 },
  checkbox: { fontSize: 18, color: '#00C6AE', marginRight: 6 },
  protocolText: { color: '#888', fontSize: 13 },
  link: { color: '#00C6AE' },
}); 