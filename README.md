# ���尲�s�D�����t�� Fake News Classifier (Taiwan TFC Version)

���M�צ��b�إߤ@�Өϥξ����ǲߪ����s�D�����t�ΡA��ƨӷ����u[�x�W�ƹ�d�֤��ߡ]TFC�^](https://tfc-taiwan.org.tw/)�v�C�z�L����۵M�y���B�z�]NLP�^�޳N�P�����ҫ��A��U�ϥΪ̿�O�s�D��T���u���C

---

## ? �M�ׯS��

- ? ����y�ơG�����x�W���a���s�D��M���
- ? �����ǲߡG�ϥ� TF-IDF + Naive Bayes �i�����
- ? NLP �B�z�G���X jieba �����P���就�ε���
- ? �i�� Streamlit Web App �@�����ʤ���

---

## ?? �M�׸�Ƨ����c

```plaintext
fake_news_project/
�u�w�w data/                      # �x�s��l�P�B�z�L�����
�x   �u�w�w raw/                  # ��l���U�Ӫ��s�D�P�е���ơ]HTML / JSON�^
�x   �u�w�w processed/            # �M�z�᪺��ơ]CSV / JSON�^
�x   �|�w�w stopwords/            # ���就�ε��C��].txt�^
�x
�u�w�w notebooks/                # ���R�P���� Jupyter ���O��
�x   �u�w�w 01_data_exploration.ipynb    # ��Ʊ����P���R
�x   �u�w�w 02_preprocessing.ipynb       # ��ƲM�z�P�_��
�x   �u�w�w 03_model_training.ipynb      # �ҫ��V�m�]TF-IDF + Naive Bayes���^
�x   �|�w�w 04_evaluation.ipynb          # �ҫ������P��ı��
�x
�u�w�w src/                      # Python �Ҳխ�l�X
�x   �u�w�w crawler/              # �������μҲ�
�x   �x   �|�w�w tfc_crawler.py    # �����x�W�ƹ�d�֤��߷s�D
�x   �u�w�w preprocessing/        # �M�z�P�_���Ҳ�
�x   �x   �|�w�w clean_text.py     # ����M�z�P jieba ����
�x   �u�w�w features/             # �S�x�u�{
�x   �x   �|�w�w vectorizer.py     # TF-IDF �إ߻P�x�s
�x   �|�w�w model/                # �ҫ��V�m�P�w���Ҳ�
�x       �|�w�w train_model.py    # �V�m�P�O�s�ҫ�
�x
�u�w�w app/                      # �̲׮i�ܥΪ� Web App�]�i�� Streamlit�^
�x   �|�w�w app.py                # UI �i�K�s�D�P�_�u��
�x
�u�w�w outputs/                  # ���G�B�Ϫ�P�ҫ�
�x   �u�w�w figures/              # �V�c�x�}�BROC ���u���Ϫ�
�x   �u�w�w models/               # �x�s�V�m�n���ҫ� (.pkl)
�x   �|�w�w logs/                 # �V�m�L�{�����O���P log
�x
�u�w�w requirements.txt          # �M��ݨD�ɮס]pip install -r�^
�u�w�w README.md                 # �M�׻���
�|�w�w .gitignore                # �����L���ɮ�
������

---

## �ϥΧ޳N

- Python 3.10+
- jieba �������
- scikit-learn
- pandas / numpy
- matplotlib / seaborn
- Streamlit�]�i��ΨӮi�ܵ��G�^

---

##  �ֳt�}�l 

1. **�w�ˮM��**

```bash
pip install -r requirements.txt