import React, { useEffect, useState } from 'react';
import { FlatList, View, StyleSheet } from 'react-native';
import { experiences as mockExperiences } from '../mock/experiences';
import ExperienceCard from '../components/ExperienceCard';

export default function HomeScreen({ navigation, route }) {
  const [expList, setExpList] = useState(mockExperiences);

  useEffect(() => {
    if (route?.params?.newExperience) {
      setExpList(prev => [route.params.newExperience, ...prev]);
      // 清除参数，避免重复添加
      navigation.setParams({ newExperience: undefined });
    }
  }, [route?.params?.newExperience]);

  return (
    <View style={styles.container}>
      <FlatList
        data={expList}
        keyExtractor={item => item.id.toString()}
        renderItem={({ item }) => (
          <ExperienceCard
            experience={item}
            onPress={() => navigation.navigate('经验详情', { experience: item })}
          />
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F6F7FB', padding: 10 },
});
