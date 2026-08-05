import React, { createContext, useCallback, useContext, useMemo, useState } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { URL_BASE } from '../config/backend';

export const NotificationContext = createContext();

const URL_NOTIFICATIONS = URL_BASE.endsWith('/') ? `${URL_BASE}notifications` : `${URL_BASE}/notifications`;

export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([]);
  const [loadingNotifications, setLoadingNotifications] = useState(true);

  const loadNotifications = useCallback(async () => {
    try {
      const usuarioId = await AsyncStorage.getItem('idUsuario');
      if (!usuarioId) {
        setNotifications([]);
        setLoadingNotifications(false);
        return;
      }

      setLoadingNotifications(true);
      const response = await fetch(`${URL_NOTIFICATIONS}?usuarioId=${usuarioId}`);
      if (!response.ok) {
        throw new Error('Falha ao carregar notificações.');
      }

      const data = await response.json();
      const mapped = data.map((item) => ({
        ...item,
        isNova: item.lida === false,
        telaDestino: item.telaDestino || (item.tipo === 'Forum' ? 'Conversa' : 'Eventos'),
        parametros: item.parametros || {},
      }));

      setNotifications(mapped);
    } catch (error) {
      console.error('Erro ao carregar notificações:', error.message);
    } finally {
      setLoadingNotifications(false);
    }
  }, []);

  const markAsRead = useCallback(async (notificationId) => {
    try {
      const usuarioId = await AsyncStorage.getItem('idUsuario');
      if (!usuarioId) return;

      setNotifications((current) =>
        current.map((item) =>
          item.id === notificationId ? { ...item, isNova: false, lida: true } : item
        )
      );

      await fetch(`${URL_NOTIFICATIONS}/${notificationId}/read`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ usuarioId }),
      });
    } catch (error) {
      console.error('Erro ao marcar notificação como lida:', error.message);
    }
  }, []);

  const markAllAsRead = useCallback(async () => {
    try {
      const usuarioId = await AsyncStorage.getItem('idUsuario');
      if (!usuarioId) return;

      setNotifications((current) => current.map((item) => ({ ...item, isNova: false, lida: true })));

      await fetch(`${URL_NOTIFICATIONS}/mark-all-read`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ usuarioId }),
      });
    } catch (error) {
      console.error('Erro ao marcar todas as notificações como lidas:', error.message);
    }
  }, []);

  const totalNovas = useMemo(
    () => notifications.filter((item) => item.isNova).length,
    [notifications]
  );

  return (
    <NotificationContext.Provider
      value={{
        notifications,
        loadingNotifications,
        totalNovas,
        loadNotifications,
        markAsRead,
        markAllAsRead,
      }}
    >
      {children}
    </NotificationContext.Provider>
  );
};

export const useNotifications = () => useContext(NotificationContext);
