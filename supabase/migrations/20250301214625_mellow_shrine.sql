/*
  # Create storage buckets for file uploads

  1. New Storage Buckets
    - `avatars` - For user profile pictures
    - `prescriptions` - For prescription files and documents

  2. Security
    - Set up RLS policies for bucket access
*/

-- Create avatars bucket
INSERT INTO storage.buckets (id, name, public)
VALUES ('avatars', 'avatars', true)
ON CONFLICT (id) DO NOTHING;

-- Create prescriptions bucket
INSERT INTO storage.buckets (id, name, public)
VALUES ('prescriptions', 'prescriptions', true)
ON CONFLICT (id) DO NOTHING;

-- Set up RLS policies for avatars bucket
CREATE POLICY "Avatar files are publicly accessible"
  ON storage.objects
  FOR SELECT
  USING (bucket_id = 'avatars');