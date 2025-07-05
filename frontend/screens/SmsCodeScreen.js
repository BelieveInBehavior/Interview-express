import React, { useState, useRef, useEffect } from 'react';
import { View, Text, TextInput, Button, StyleSheet, TouchableOpacity, Alert } from 'react-native';
import apiService from '../services/api';

export default function SmsCodeScreen({ navigation, route }) {
  const { phone } = route.params || {};
  const [code, setCode] = useState('');
  const [timer, setTimer] = useState(60);
  const [loading, setLoading] = useState(false);
  const timerRef = useRef();

  useEffect(() => {
    if (timer > 0) {
      timerRef.current = setTimeout(() => setTimer(timer - 1), 1000);
    }
    return () => clearTimeout(timerRef.current);
  }, [timer]);

  const handleResend = async () => {
    if (timer > 0) return;
    setTimer(60);
    try {
      await apiService.sendSmsCode(phone);
      Alert.alert('验证码已重新发送');
    } catch (error) {
      Alert.alert('发送验证码失败', error.message);
    }
  };

  const handleNext = async () => {
    if (code.length !== 4) {
      Alert.alert('请输入4位验证码');
      return;
    }

    setLoading(true);
    try {
      const response = await apiService.login(phone, code);
      // 登录成功，跳转到主页面
      navigation.reset({
        index: 0,
        routes: [{ name: 'Main' }],
      });
    } catch (error) {
      Alert.alert('登录失败', error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.logo}>面经快车</Text>
      <Text style={styles.title}>输入短信验证码</Text>
      <Text style={styles.desc}>已向您的手机 {phone?.slice(-4)} 发送验证码</Text>
      <View style={styles.codeRow}>
        <TextInput
          style={styles.codeInput}
          placeholder=""
          keyboardType="number-pad"
          maxLength={4}
          value={code}
          onChangeText={setCode}
        />
      </View>
      <View style={styles.resendRow}>
        <TouchableOpacity disabled={timer > 0} onPress={handleResend}>
          <Text style={[styles.resendText, timer > 0 && { color: '#bbb' }]}>重新发送{timer > 0 ? `（${timer}）` : ''}</Text>
        </TouchableOpacity>
      </View>
      <TouchableOpacity 
        style={[styles.nextBtn, loading && styles.nextBtnDisabled]} 
        onPress={handleNext}
        disabled={loading}
      >
        <Text style={styles.nextBtnText}>{loading ? '登录中...' : '下一步'}</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', padding: 24 },
  logo: { color: '#00C6AE', fontWeight: 'bold', fontSize: 22, alignSelf: 'center', marginTop: 16, marginBottom: 24 },
  title: { fontSize: 26, fontWeight: 'bold', marginBottom: 8 },
  desc: { color: '#888', marginBottom: 32 },
  codeRow: { flexDirection: 'row', justifyContent: 'center', marginBottom: 16 },
  codeInput: { fontSize: 28, letterSpacing: 24, backgroundColor: '#F6F7FB', borderRadius: 8, padding: 12, width: 180, textAlign: 'center' },
  resendRow: { alignItems: 'center', marginBottom: 24 },
  resendText: { color: '#00C6AE', fontSize: 15 },
  nextBtn: { backgroundColor: '#00C6AE', borderRadius: 8, marginTop: 8, marginBottom: 16, height: 48, justifyContent: 'center', alignItems: 'center' },
  nextBtnDisabled: { backgroundColor: '#ccc' },
  nextBtnText: { color: '#fff', fontSize: 20 },
}); 