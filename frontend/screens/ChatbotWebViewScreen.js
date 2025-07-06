import React from 'react';
import { StyleSheet, View, Platform } from 'react-native';

let ChatbotContent;
if (Platform.OS === 'web') {
  // Web端用iframe
  ChatbotContent = () => (
    <iframe
      src="https://udify.app/chatbot/bseA6RA5CxsacpHE"
      style={{ width: '100%', height: '100%', minHeight: 700, border: 'none' }}
      allow="microphone"
      title="模拟面试"
    />
  );
} else {
  // 原生端用WebView
  const { WebView } = require('react-native-webview');
  ChatbotContent = () => (
    <WebView
      source={{ uri: 'https://udify.app/chatbot/bseA6RA5CxsacpHE' }}
      style={{ flex: 1 }}
      javaScriptEnabled
      domStorageEnabled
      allowsInlineMediaPlayback
      mediaPlaybackRequiresUserAction={false}
      originWhitelist={['*']}
      allowsFullscreenVideo
    />
  );
}

export default function ChatbotWebViewScreen() {
  return (
    <View style={styles.container}>
      <ChatbotContent />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
});