import React, { useRef, useState } from 'react';
import { View, TextInput, Button, StyleSheet, Text, ScrollView, Alert } from 'react-native';
import { RichEditor, RichToolbar, actions } from 'react-native-pell-rich-editor';
import Slider from '@react-native-community/slider';
import { launchImageLibrary } from 'react-native-image-picker';
import apiService from '../services/api';

export default function PublishScreen({ navigation }) {
  const richText = useRef();
  const [company, setCompany] = useState('');
  const [position, setPosition] = useState('');
  const [content, setContent] = useState('');
  const [difficulty, setDifficulty] = useState(0);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!company || !position || !content) {
      Alert.alert('请填写完整信息');
      return;
    }

    setLoading(true);
    try {
      const experienceData = {
        company,
        position,
        summary: content.substring(0, 100) + '...', // 简单的摘要
        content,
        difficulty,
        tags: [] // 暂时为空，后续可以添加标签功能
      };

      await apiService.createExperience(experienceData);
      Alert.alert('发布成功', '你的经验已发布！', [
        {
          text: '确定',
          onPress: () => {
            setCompany('');
            setPosition('');
            setContent('');
            setDifficulty(0);
            // 返回首页并刷新
            navigation.navigate('首页');
          }
        }
      ]);
    } catch (error) {
      Alert.alert('发布失败', error.message);
    } finally {
      setLoading(false);
    }
  };

  // 图片插入处理
  const handleInsertImage = async () => {
    launchImageLibrary({ mediaType: 'photo' }, (response) => {
      if (response.didCancel || !response.assets || response.assets.length === 0) return;
      const imageUrl = response.assets[0].uri;
      // 这里可上传到服务器，拿到线上URL后再插入
      richText.current?.insertImage(imageUrl);
    });
  };

  return (
    <ScrollView style={styles.container} keyboardShouldPersistTaps="handled">
      <TextInput style={styles.input} placeholder="公司名称" value={company} onChangeText={setCompany} />
      <TextInput style={styles.input} placeholder="职位" value={position} onChangeText={setPosition} />
      <View style={{ flexDirection: 'row', alignItems: 'center', marginBottom: 16 }}>
        <Text style={{ marginRight: 12, width: 70 }}>难度：{difficulty}/5</Text>
        <Slider
          style={{ flex: 1, height: 40 }}
          minimumValue={0}
          maximumValue={5}
          step={1}
          value={difficulty}
          onValueChange={setDifficulty}
          minimumTrackTintColor="#00C6AE"
          maximumTrackTintColor="#eee"
          thumbTintColor="#00C6AE"
        />
      </View>
      <Text style={{ marginTop: 10, marginBottom: 5 }}>面试经验：</Text>
      <RichEditor
        ref={richText}
        style={styles.rich}
        placeholder="请输入详细面试经验"
        initialContentHTML={content}
        onChange={setContent}
      />
      <RichToolbar
        editor={richText}
        actions={[
          actions.setBold,
          actions.setItalic,
          actions.insertBulletsList,
          actions.insertOrderedList,
          actions.insertLink,
          actions.insertImage,
        ]}
        onPressAddImage={handleInsertImage}
      />
      <Button 
        title={loading ? "发布中..." : "发布"} 
        onPress={handleSubmit} 
        color="#00C6AE"
        disabled={loading}
      />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', padding: 16 },
  input: { backgroundColor: '#F6F7FB', borderRadius: 8, padding: 10, marginBottom: 10, fontSize: 16 },
  rich: { minHeight: 120, borderColor: '#eee', borderWidth: 1, borderRadius: 8, marginBottom: 10 },
});
