from setuptools import setup, find_packages

setup(
    name='desafio_iafront',
    version='',
    packages=find_packages(),
    url='',
    license='',
    author='Time IA-FRONT',
    author_email='',
    description='',
    install_requires=[
        "scikit-learn==0.23.1",
        "click==7.1.2",
        "bokeh==2.1.1",
        "dataset-loader==1.6",
        'pandas==1.1.0',
        'numpy==1.19.1'
    ],
    entry_points={
        'console_scripts': [
            'prepara-pedidos=desafio_iafront.jobs.pedidos:main',
            'cria-visitas=desafio_iafront.jobs.create_visits:main',
            'escala-visitas=desafio_iafront.jobs.escala_pedidos:main',
            'escala-analise-distribuicao-scatter=desafio_iafront.jobs.graphics:scatter_scale_analysis',
            'escala-analise-distribuicao-histograma=desafio_iafront.jobs.graphics:histogram_scale_analysis',
            'analise-conversao-temporal=desafio_iafront.jobs.graphics:analise_conversao_temporal',

            'particiona-conversao=desafio_iafront.jobs.particiona_conversao:main',
            'conversao-analise-cluster=desafio_iafront.jobs.graphics:plot_conversao',

            'agglomerative-clustering=desafio_iafront.jobs.clusters:agglomerative',
            'kmeans-clustering=desafio_iafront.jobs.clusters:kmeans',
            'optics-clustering=desafio_iafront.jobs.clusters:optics',
            'affinity-clustering=desafio_iafront.jobs.clusters:affinity',
            'spectral-clustering=desafio_iafront.jobs.clusters:spectral'

        ]
    }
)
