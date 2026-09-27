import React, { useContext, useState } from 'react';
import { Outlet, NavLink, useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { 
  LayoutDashboard, 
  Bot,
  CalendarDays, 
  CalendarRange, 
  Utensils, 
  Database,
  Heart,
  Activity, 
  ShoppingCart, 
  User, 
  Settings,
  ShieldCheck,
  Server,
  LogOut, 
  Menu, 
  X,
  Sparkles
} from 'lucide-react';

export const Layout = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const mainNavItems = [
    { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/assistant', icon: Bot, label: 'AI Assistant', badge: 'AI' },
    { to: '/meal-plan', icon: CalendarDays, label: "Today's Plan" },
    { to: '/meal-plan/weekly', icon: CalendarRange, label: 'Weekly Plan' },
    { to: '/meals', icon: Utensils, label: 'Explore Meals' },
    { to: '/foods', icon: Database, label: 'Food Database' },
    { to: '/favorites', icon: Heart, label: 'Favorites' },
    { to: '/nutrition', icon: Activity, label: 'Nutrition Targets' },
    { to: '/grocery', icon: ShoppingCart, label: 'Grocery List' },
  ];

  const secondaryNavItems = [
    { to: '/profile', icon: User, label: 'Profile' },
    { to: '/settings', icon: Settings, label: 'Settings' },
    { to: '/admin', icon: ShieldCheck, label: 'Clinical Governance' },
    { to: '/system-health', icon: Server, label: 'System Health' },
  ];

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navClasses = ({ isActive }) =>
    `flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition ${
      isActive 
        ? 'bg-emerald-50 text-emerald-700 font-semibold' 
        : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
    }`;

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/50 backdrop-blur-xs lg:hidden" 
          onClick={() => setSidebarOpen(false)} 
        />
      )}

      {/* Sidebar */}
      <aside className={`fixed lg:static inset-y-0 left-0 z-50 w-64 bg-white border-r border-slate-200 transform ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} lg:translate-x-0 transition-transform duration-200 ease-in-out flex flex-col`}>
        {/* Brand Logo Header */}
        <div className="p-5 border-b border-slate-100 flex items-center justify-between">
          <Link to="/dashboard" className="flex items-center space-x-2.5">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center text-white shadow-sm shadow-emerald-500/20">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <span className="text-lg font-extrabold tracking-tight text-slate-900">
                NutriGuard
              </span>
              <span className="block text-[10px] font-semibold text-emerald-600 -mt-0.5">
                Indian AI Nutrition
              </span>
            </div>
          </Link>
          <button 
            onClick={() => setSidebarOpen(false)} 
            className="lg:hidden p-1.5 text-slate-400 hover:text-slate-700 rounded-lg"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation Links */}
        <div className="flex-1 px-3 py-4 space-y-6 overflow-y-auto">
          <div>
            <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400 px-3 mb-2">
              Menu
            </div>
            <nav className="space-y-1">
              {mainNavItems.map((item) => (
                <NavLink 
                  key={item.to} 
                  to={item.to} 
                  onClick={() => setSidebarOpen(false)} 
                  className={navClasses}
                >
                  <div className="flex items-center space-x-3">
                    <item.icon className="w-4 h-4" />
                    <span>{item.label}</span>
                  </div>
                  {item.badge && (
                    <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800">
                      {item.badge}
                    </span>
                  )}
                </NavLink>
              ))}
            </nav>
          </div>

          <div>
            <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400 px-3 mb-2">
              System & Settings
            </div>
            <nav className="space-y-1">
              {secondaryNavItems.map((item) => (
                <NavLink 
                  key={item.to} 
                  to={item.to} 
                  onClick={() => setSidebarOpen(false)} 
                  className={navClasses}
                >
                  <div className="flex items-center space-x-3">
                    <item.icon className="w-4 h-4" />
                    <span>{item.label}</span>
                  </div>
                </NavLink>
              ))}
            </nav>
          </div>
        </div>

        {/* User Card & Logout Footer */}
        <div className="p-3 border-t border-slate-100">
          <div className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-100">
            <div className="flex items-center space-x-2.5 min-w-0">
              <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center text-white text-xs font-bold">
                {user?.name?.charAt(0) || user?.email?.charAt(0) || 'U'}
              </div>
              <div className="min-w-0">
                <p className="text-xs font-semibold text-slate-800 truncate">{user?.name || 'User'}</p>
                <p className="text-[10px] text-slate-400 truncate">{user?.email || 'Logged in'}</p>
              </div>
            </div>
            <button 
              onClick={handleLogout} 
              className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition"
              title="Sign Out"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Mobile Header */}
        <header className="bg-white border-b border-slate-200 lg:hidden flex items-center justify-between p-4 sticky top-0 z-30">
          <div className="flex items-center space-x-2">
            <div className="w-7 h-7 rounded-lg bg-emerald-600 flex items-center justify-center text-white">
              <ShieldCheck className="w-4 h-4" />
            </div>
            <h1 className="text-base font-bold text-slate-900">NutriGuard</h1>
          </div>
          <button 
            onClick={() => setSidebarOpen(true)} 
            className="p-2 text-slate-600 hover:bg-slate-100 rounded-lg"
          >
            <Menu className="w-5 h-5" />
          </button>
        </header>

        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
