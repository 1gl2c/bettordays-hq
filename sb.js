// Shared Supabase client for bettordays.xyz. The publishable key is safe to ship to browsers;
// every table is protected by row level security in the database.
window.BD_SB = window.supabase.createClient(
  'https://ndcsjhetuasijbgpfhwj.supabase.co',
  'sb_publishable_thFDxFfsdTESdl_MzPeE3g_pUqcSMRc',
  { auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true } }
);
