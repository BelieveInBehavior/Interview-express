import * as React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { Provider as PaperProvider } from 'react-native-paper';
import Icon from 'react-native-vector-icons/Ionicons';

import HomeScreen from './screens/HomeScreen';
import SearchScreen from './screens/SearchScreen';
import PublishScreen from './screens/PublishScreen';
import ExperienceDetailScreen from './screens/ExperienceDetailScreen';
import LoginScreen from './screens/LoginScreen';
import SmsCodeScreen from './screens/SmsCodeScreen';
import ChatbotWebViewScreen from './screens/ChatbotWebViewScreen';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

function MainTabs({ navigation }) {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ color, size }) => {
          let iconName;
          if (route.name === '首页') iconName = 'home-outline';
          else if (route.name === '搜索') iconName = 'search-outline';
          else if (route.name === '发布') iconName = 'add-circle-outline';
          else if (route.name === '模拟面试') iconName = 'chatbubble-ellipses-outline';
          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#00C6AE',
        tabBarInactiveTintColor: 'gray',
      })}
    >
      <Tab.Screen name="首页" component={HomeScreen} />
      <Tab.Screen name="搜索" component={SearchScreen} />
      <Tab.Screen name="发布" component={PublishScreen} />
      <Tab.Screen
        name="模拟面试"
        component={() => null}
        listeners={({ navigation }) => ({
          tabPress: e => {
            e.preventDefault();
            navigation.navigate('模拟面试Web');
          }
        })}
        options={{
          tabBarLabel: '模拟面试',
        }}
      />
    </Tab.Navigator>
  );
}

export default function App() {
  return (
    <PaperProvider>
      <NavigationContainer>
        <Stack.Navigator initialRouteName="登录">
          <Stack.Screen name="登录" component={LoginScreen} options={{ headerShown: false }} />
          <Stack.Screen name="验证码" component={SmsCodeScreen} options={{ headerShown: false }} />
          <Stack.Screen name="Main" component={MainTabs} options={{ headerShown: false }} />
          <Stack.Screen name="经验详情" component={ExperienceDetailScreen} />
          <Stack.Screen name="模拟面试Web" component={ChatbotWebViewScreen} options={{ title: '模拟面试' }} />
        </Stack.Navigator>
      </NavigationContainer>
    </PaperProvider>
  );
}
