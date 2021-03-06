PGDMP     5    9    
        
    t            control_vehicular    9.4.4    9.4.1 C    M           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false            N           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false            O           1262    16387    control_vehicular    DATABASE     �   CREATE DATABASE control_vehicular WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';
 !   DROP DATABASE control_vehicular;
          	   homestead    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             postgres    false            P           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  postgres    false    5            Q           0    0    public    ACL     �   REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;
                  postgres    false    5            �            3079    11893    plpgsql 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
    DROP EXTENSION plpgsql;
                  false            R           0    0    EXTENSION plpgsql    COMMENT     @   COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
                       false    187            �            1259    16507    camara_backup    TABLE     �   CREATE TABLE camara_backup (
    id integer NOT NULL,
    ip character varying(255),
    lugar_id integer NOT NULL,
    created_at timestamp(0) without time zone NOT NULL,
    updated_at timestamp(0) without time zone NOT NULL
);
 !   DROP TABLE public.camara_backup;
       public      	   homestead    false    5            �            1259    16505    camara_id_seq    SEQUENCE     o   CREATE SEQUENCE camara_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.camara_id_seq;
       public    	   homestead    false    179    5            S           0    0    camara_id_seq    SEQUENCE OWNED BY     8   ALTER SEQUENCE camara_id_seq OWNED BY camara_backup.id;
            public    	   homestead    false    178            �            1259    57350    camara    TABLE     
  CREATE TABLE camara (
    id integer DEFAULT nextval('camara_id_seq'::regclass) NOT NULL,
    ip character varying(255),
    lugar_id integer NOT NULL,
    created_at timestamp(0) without time zone NOT NULL,
    updated_at timestamp(0) without time zone NOT NULL
);
    DROP TABLE public.camara;
       public      	   homestead    false    178    5            �            1259    16471    lugar    TABLE     �   CREATE TABLE lugar (
    id integer NOT NULL,
    nombre character varying(255) NOT NULL,
    created_at timestamp(0) without time zone NOT NULL,
    updated_at timestamp(0) without time zone NOT NULL
);
    DROP TABLE public.lugar;
       public      	   homestead    false    5            �            1259    16469    lugar_id_seq    SEQUENCE     n   CREATE SEQUENCE lugar_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.lugar_id_seq;
       public    	   homestead    false    177    5            T           0    0    lugar_id_seq    SEQUENCE OWNED BY     /   ALTER SEQUENCE lugar_id_seq OWNED BY lugar.id;
            public    	   homestead    false    176            �            1259    16522    miembro    TABLE     '  CREATE TABLE miembro (
    id integer NOT NULL,
    nombres character varying(255) NOT NULL,
    apellidos character varying(255) NOT NULL,
    cod_administrativo integer NOT NULL,
    created_at timestamp(0) without time zone NOT NULL,
    updated_at timestamp(0) without time zone NOT NULL
);
    DROP TABLE public.miembro;
       public      	   homestead    false    5            �            1259    16520    miembro_id_seq    SEQUENCE     p   CREATE SEQUENCE miembro_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.miembro_id_seq;
       public    	   homestead    false    181    5            U           0    0    miembro_id_seq    SEQUENCE OWNED BY     3   ALTER SEQUENCE miembro_id_seq OWNED BY miembro.id;
            public    	   homestead    false    180            �            1259    16413 
   migrations    TABLE     g   CREATE TABLE migrations (
    migration character varying(255) NOT NULL,
    batch integer NOT NULL
);
    DROP TABLE public.migrations;
       public      	   homestead    false    5            �            1259    16461    password_resets    TABLE     �   CREATE TABLE password_resets (
    email character varying(255) NOT NULL,
    token character varying(255) NOT NULL,
    created_at timestamp(0) without time zone NOT NULL
);
 #   DROP TABLE public.password_resets;
       public      	   homestead    false    5            �            1259    49193    placa    TABLE     �   CREATE TABLE placa (
    id integer NOT NULL,
    numero character varying(255) NOT NULL,
    miembro_id integer NOT NULL,
    created_at timestamp(0) without time zone NOT NULL,
    updated_at timestamp(0) without time zone NOT NULL
);
    DROP TABLE public.placa;
       public      	   homestead    false    5            �            1259    49191    placa_id_seq    SEQUENCE     n   CREATE SEQUENCE placa_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.placa_id_seq;
       public    	   homestead    false    5    183            V           0    0    placa_id_seq    SEQUENCE OWNED BY     /   ALTER SEQUENCE placa_id_seq OWNED BY placa.id;
            public    	   homestead    false    182            �            1259    49253    registro    TABLE     �  CREATE TABLE registro (
    id integer NOT NULL,
    camara character varying(255) NOT NULL,
    lugar character varying(255) NOT NULL,
    filename character varying(255) NOT NULL,
    placa character varying(255) NOT NULL,
    created_at timestamp(0) without time zone NOT NULL,
    updated_at timestamp(0) without time zone NOT NULL,
    mime character varying(255) NOT NULL,
    miembro character varying(255),
    mismatch boolean
);
    DROP TABLE public.registro;
       public      	   homestead    false    5            �            1259    49251    registro_id_seq    SEQUENCE     q   CREATE SEQUENCE registro_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.registro_id_seq;
       public    	   homestead    false    5    185            W           0    0    registro_id_seq    SEQUENCE OWNED BY     5   ALTER SEQUENCE registro_id_seq OWNED BY registro.id;
            public    	   homestead    false    184            �            1259    16450    users    TABLE     M  CREATE TABLE users (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password character varying(60) NOT NULL,
    remember_token character varying(100),
    created_at timestamp(0) without time zone NOT NULL,
    updated_at timestamp(0) without time zone NOT NULL
);
    DROP TABLE public.users;
       public      	   homestead    false    5            �            1259    16448    users_id_seq    SEQUENCE     n   CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public    	   homestead    false    174    5            X           0    0    users_id_seq    SEQUENCE OWNED BY     /   ALTER SEQUENCE users_id_seq OWNED BY users.id;
            public    	   homestead    false    173            �           2604    16510    id    DEFAULT     _   ALTER TABLE ONLY camara_backup ALTER COLUMN id SET DEFAULT nextval('camara_id_seq'::regclass);
 ?   ALTER TABLE public.camara_backup ALTER COLUMN id DROP DEFAULT;
       public    	   homestead    false    178    179    179            �           2604    16474    id    DEFAULT     V   ALTER TABLE ONLY lugar ALTER COLUMN id SET DEFAULT nextval('lugar_id_seq'::regclass);
 7   ALTER TABLE public.lugar ALTER COLUMN id DROP DEFAULT;
       public    	   homestead    false    177    176    177            �           2604    16525    id    DEFAULT     Z   ALTER TABLE ONLY miembro ALTER COLUMN id SET DEFAULT nextval('miembro_id_seq'::regclass);
 9   ALTER TABLE public.miembro ALTER COLUMN id DROP DEFAULT;
       public    	   homestead    false    181    180    181            �           2604    49196    id    DEFAULT     V   ALTER TABLE ONLY placa ALTER COLUMN id SET DEFAULT nextval('placa_id_seq'::regclass);
 7   ALTER TABLE public.placa ALTER COLUMN id DROP DEFAULT;
       public    	   homestead    false    183    182    183            �           2604    49256    id    DEFAULT     \   ALTER TABLE ONLY registro ALTER COLUMN id SET DEFAULT nextval('registro_id_seq'::regclass);
 :   ALTER TABLE public.registro ALTER COLUMN id DROP DEFAULT;
       public    	   homestead    false    184    185    185            �           2604    16453    id    DEFAULT     V   ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public    	   homestead    false    173    174    174            J          0    57350    camara 
   TABLE DATA               C   COPY camara (id, ip, lugar_id, created_at, updated_at) FROM stdin;
    public    	   homestead    false    186   H       C          0    16507    camara_backup 
   TABLE DATA               J   COPY camara_backup (id, ip, lugar_id, created_at, updated_at) FROM stdin;
    public    	   homestead    false    179   |H       Y           0    0    camara_id_seq    SEQUENCE SET     5   SELECT pg_catalog.setval('camara_id_seq', 21, true);
            public    	   homestead    false    178            A          0    16471    lugar 
   TABLE DATA               <   COPY lugar (id, nombre, created_at, updated_at) FROM stdin;
    public    	   homestead    false    177   �H       Z           0    0    lugar_id_seq    SEQUENCE SET     4   SELECT pg_catalog.setval('lugar_id_seq', 25, true);
            public    	   homestead    false    176            E          0    16522    miembro 
   TABLE DATA               ^   COPY miembro (id, nombres, apellidos, cod_administrativo, created_at, updated_at) FROM stdin;
    public    	   homestead    false    181   �I       [           0    0    miembro_id_seq    SEQUENCE SET     5   SELECT pg_catalog.setval('miembro_id_seq', 7, true);
            public    	   homestead    false    180            <          0    16413 
   migrations 
   TABLE DATA               /   COPY migrations (migration, batch) FROM stdin;
    public    	   homestead    false    172   UJ       ?          0    16461    password_resets 
   TABLE DATA               <   COPY password_resets (email, token, created_at) FROM stdin;
    public    	   homestead    false    175   K       G          0    49193    placa 
   TABLE DATA               H   COPY placa (id, numero, miembro_id, created_at, updated_at) FROM stdin;
    public    	   homestead    false    183   2K       \           0    0    placa_id_seq    SEQUENCE SET     3   SELECT pg_catalog.setval('placa_id_seq', 3, true);
            public    	   homestead    false    182            I          0    49253    registro 
   TABLE DATA               p   COPY registro (id, camara, lugar, filename, placa, created_at, updated_at, mime, miembro, mismatch) FROM stdin;
    public    	   homestead    false    185   �K       ]           0    0    registro_id_seq    SEQUENCE SET     8   SELECT pg_catalog.setval('registro_id_seq', 140, true);
            public    	   homestead    false    184            >          0    16450    users 
   TABLE DATA               [   COPY users (id, name, email, password, remember_token, created_at, updated_at) FROM stdin;
    public    	   homestead    false    174   W       ^           0    0    users_id_seq    SEQUENCE SET     4   SELECT pg_catalog.setval('users_id_seq', 1, false);
            public    	   homestead    false    173            �           2606    16519    camara_ip_unique 
   CONSTRAINT     P   ALTER TABLE ONLY camara_backup
    ADD CONSTRAINT camara_ip_unique UNIQUE (ip);
 H   ALTER TABLE ONLY public.camara_backup DROP CONSTRAINT camara_ip_unique;
       public      	   homestead    false    179    179            �           2606    16512    camara_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY camara_backup
    ADD CONSTRAINT camara_pkey PRIMARY KEY (id);
 C   ALTER TABLE ONLY public.camara_backup DROP CONSTRAINT camara_pkey;
       public      	   homestead    false    179    179            �           2606    57355    camara_pkey_2 
   CONSTRAINT     K   ALTER TABLE ONLY camara
    ADD CONSTRAINT camara_pkey_2 PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.camara DROP CONSTRAINT camara_pkey_2;
       public      	   homestead    false    186    186            �           2606    16478    lugar_nombre_unique 
   CONSTRAINT     O   ALTER TABLE ONLY lugar
    ADD CONSTRAINT lugar_nombre_unique UNIQUE (nombre);
 C   ALTER TABLE ONLY public.lugar DROP CONSTRAINT lugar_nombre_unique;
       public      	   homestead    false    177    177            �           2606    16476 
   lugar_pkey 
   CONSTRAINT     G   ALTER TABLE ONLY lugar
    ADD CONSTRAINT lugar_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.lugar DROP CONSTRAINT lugar_pkey;
       public      	   homestead    false    177    177            �           2606    16532 !   miembro_cod_administrativo_unique 
   CONSTRAINT     k   ALTER TABLE ONLY miembro
    ADD CONSTRAINT miembro_cod_administrativo_unique UNIQUE (cod_administrativo);
 S   ALTER TABLE ONLY public.miembro DROP CONSTRAINT miembro_cod_administrativo_unique;
       public      	   homestead    false    181    181            �           2606    16530    miembro_pkey 
   CONSTRAINT     K   ALTER TABLE ONLY miembro
    ADD CONSTRAINT miembro_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.miembro DROP CONSTRAINT miembro_pkey;
       public      	   homestead    false    181    181            �           2606    49205    placa_numero_unique 
   CONSTRAINT     O   ALTER TABLE ONLY placa
    ADD CONSTRAINT placa_numero_unique UNIQUE (numero);
 C   ALTER TABLE ONLY public.placa DROP CONSTRAINT placa_numero_unique;
       public      	   homestead    false    183    183            �           2606    49198 
   placa_pkey 
   CONSTRAINT     G   ALTER TABLE ONLY placa
    ADD CONSTRAINT placa_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.placa DROP CONSTRAINT placa_pkey;
       public      	   homestead    false    183    183            �           2606    49261    registro_pkey 
   CONSTRAINT     M   ALTER TABLE ONLY registro
    ADD CONSTRAINT registro_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.registro DROP CONSTRAINT registro_pkey;
       public      	   homestead    false    185    185            �           2606    16460    users_email_unique 
   CONSTRAINT     M   ALTER TABLE ONLY users
    ADD CONSTRAINT users_email_unique UNIQUE (email);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_unique;
       public      	   homestead    false    174    174            �           2606    16458 
   users_pkey 
   CONSTRAINT     G   ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public      	   homestead    false    174    174            �           1259    16467    password_resets_email_index    INDEX     Q   CREATE INDEX password_resets_email_index ON password_resets USING btree (email);
 /   DROP INDEX public.password_resets_email_index;
       public      	   homestead    false    175            �           1259    16468    password_resets_token_index    INDEX     Q   CREATE INDEX password_resets_token_index ON password_resets USING btree (token);
 /   DROP INDEX public.password_resets_token_index;
       public      	   homestead    false    175            �           2606    16513    camara_lugar_id_foreign    FK CONSTRAINT     �   ALTER TABLE ONLY camara_backup
    ADD CONSTRAINT camara_lugar_id_foreign FOREIGN KEY (lugar_id) REFERENCES lugar(id) ON DELETE CASCADE;
 O   ALTER TABLE ONLY public.camara_backup DROP CONSTRAINT camara_lugar_id_foreign;
       public    	   homestead    false    1979    177    179            �           2606    57356    camara_lugar_id_foreign_2    FK CONSTRAINT     �   ALTER TABLE ONLY camara
    ADD CONSTRAINT camara_lugar_id_foreign_2 FOREIGN KEY (lugar_id) REFERENCES lugar(id) ON DELETE CASCADE;
 J   ALTER TABLE ONLY public.camara DROP CONSTRAINT camara_lugar_id_foreign_2;
       public    	   homestead    false    186    177    1979            �           2606    49199    placa_miembro_id_foreign    FK CONSTRAINT     �   ALTER TABLE ONLY placa
    ADD CONSTRAINT placa_miembro_id_foreign FOREIGN KEY (miembro_id) REFERENCES miembro(id) ON DELETE CASCADE;
 H   ALTER TABLE ONLY public.placa DROP CONSTRAINT placa_miembro_id_foreign;
       public    	   homestead    false    181    1987    183            J   V   x�m��� �v4��]�(�
迎@)�y��@�9:"{�`r�/'�tA�!ns� ����v/'��n�_&Խ{���4U} L��      C   \   x�m���0���]�Q���Y��BB�˲7��!w�a�`
с��^\�۟���)x3gê�����
>�yW�=:ш��NS��4 �      A   �   x�m��n�@��ۧ��v���� E����DC~D��cc� s��ivg��T�_?���X �b��H�I�	J7�?��h�9&���j3�;��,DS�c��l�~��Ԁ� T�ny�[]�é�e��`] �d9&�{�=W�]g�[eXL�C&Hm��F{o>=G��� �Gh|@w��	C�������4e�	�����"o�f���XD��d      E   }   x�m�1
�0�W�w�H�@ M�iӜa�L��>��U�����S��fP�8��'N9��W�Q���V�ڳ-��������(��Zl3L�۠�h��L#�bϽ�/D��.�1z���{�3�      <   �   x�u��
�0���cF���2U���*��Ui',���$X	� 	\#�wvwr�춛����ޫĻ��"�g@�r�:�c����@\_!1f���z���-���-�_�l������J��m��Qf�όS����S��/h���cN�M�o�hj��F��J�7t�      ?      x������ � �      G   I   x�3�43�p��4�4204�50�50V02�25�2��&�e�idhb���i�"#C+S+SClb\1z\\\ TI�      I   r  x��Zێ]�}�|��MUߪ�(A����"K"��V�3�t�s�lF����Ruպ���^1�k�zï����W��L�H���Q�IJj,Q�k��o���O�������%���az�����������S�l����/�b�{W�����o�.ƨ���\��1�ɪ��Бmom��!lk1DZ0(�t��!I4>Q1�|5��\5�6Z����0ȶ���������������ӻ���>�_������y	}�)<LFs��b�{4���m���ɍ������L&q��}�Lb��ï�q'������VQpΙ2r6�6%u�	R[ͩk��<mk�1�uDb�	kJW\��l�+��l�����uv[��!.:Dl���!&�M��kj7�18N����g�q:��wq��Y�8��`en�v�S��1Z�Ey�#v��z��'z~-��8+����<���\��hO��VW�$�<�Y�����йv ���B��z4%�n|�+ٌK���@)����ˇ��_�V�����[p�]\I6jm�)��9k�j��i��Xھ9��)�'���m4��&UbW\1�&�
��A��F)-������Y��a�Rĸ1^s4)�k�9�>6��f=�7X�6���deې"��f��!�T���B6d�kX,ok��İbQ'4�s�	�!�	=k��&ga��ok�IV��8��!�D����;�k��Zm�ᖂ�����'�OΟX��3���$gSu�!�	:��fS�t�.�4��@����]m��Z���3��eSe8�=���u4�����4�J���lQ �1�8댃�������S,r��$�ځ}Z5���1��:��Q)�3��hL1;s>Y���Y%
")1���)�)Ք�,��L��{S�����֞��֜k����ԅ����T!U�c���jQ�����E����n[�}Mi�2,P�d��'z���6�	��%��G������`V=���JD&�J`;͐�3�$����`6��m� ��t�$�i#�/��������/�sӶv �J���Q�d!��S�"#����v��Q|t{Ok�l�W��hC�K��`n!UE%FF���`��|�m:y��noRZ��UPI��4?<B	�+�I0��K=R�/Z�����MG�hV�6";�23=B�VD�i�r�4�l<�'?��s� ���Ly��s�ih�(���2�Vj�/0,���lkЬg̉��zã��O�u�\�_q�nk�lL9����4��W,S.P|�8����hok���J{��"�C���ME�eN��J蘕إ�����W��v �J|��Wd������]���
9��ز��_<l_B�<>L=� �2����1���fL�|�ɭF���^��|�'���$Id"g�OAzv�>���W�söv �J|1w��ш����I| ��[�=��*��`Yi�VF�E H-�����1/�ڃ��ڧ�iP~�ӕ�"�!�!6OZ3���#MJ�kma���ee<"�l���L�n�Z�E����JkW�lF��R�|'݇�0�4g�����j�wBFa�Ƈ=���0��\H�������\9��٭v��(/��8+�b��'N��!L��gDJ�/ge`+.�p6-x�L��Ins�So7�m����%G���9c�:�(�6��@5W�\_������=�ͷ��	e�\8k/v��d�'nkG�D�P��5Le>��N)WIc��Z�C���	�$���v���8յ]���>�ymXy[�rF��]��<Z��#pV>����x��ip.��
3�R���hVF�h&d�3:��Ֆn��T��Ԑ_
�ƃڒBuθ��?�Y�˨�K����=��n��m��r2���4!d�al���T�z�;�y`��^7&���;���6�U.3�λ�D(�ɐH�{�=okGଜ\rwCГ2"���`��y1̟o����pVN�:^g�j�� ��l�OQ].I��mkG�l8�"�����i�p��
)��#	��\�]�f�&Н[#���H�&��t�\ˍބm��ݛ,�M�f����摬�wF�~$'q�䏇�2���^��~jh��P�.n~W&���U��������2��+�dF���&Մ|W�g���Fs>�J��J��B3� l92�fB«.�g�Z݀�p�=�f�v�!��v�!#s�V���>��$;+���l~9�ّt���<��f�լ��o8�P�b�R2앳�{�8��n�%#'�ѹ��s���8��d�o̬�0�|�c8Tx$.�`aKs��X�!A>D�vedr������	���
���B�j��W}�'�Y9��*e���~f!����d����1ɼ!A>D�v�d$rO����$���Q�������-[4�d�ɹ�A�Rr�~���H�aur��0�Uq���;WG�m��W����m����|�c%�F�VW��l���t����l|�A��e?��rSV*�9.C"M�8�"�F�|k�T��+ZbU8��������I�4���|�.\
	V����x0+CH�����"T���6K�,T��;���
&mkG��,,!������L��k�+�7_���G�{/6�/�-"X�ܑ�=��	�t��WH8�mkGЬ$�%�R�55h��V�R�7Qx��l~�ď�F�1�_�J��كS�D���lH�"=�RpV�b�-/��l�Sj���s%Շ'�K��	pV����De��`�Mj2K�`���Sn�}������U%@4ɡ7�����,I*=JO����уpVAp+w������D��$��RBI�s�D���x�����2�Ts��£�=�"�-�1��?Ǐo����P�j�      >      x������ � �     