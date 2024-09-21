# `class transformers.TrainingArguments`

params:

* output_dir:
* evaluation_stategy (defaults to 'no'):
  - no
  - steps: via `eval_steps` param
  - epoch:
* per_device_train_batch_size
* per_device_eval_batch_size
* learning_rate: defaults to 5e-5, for `AdamW` optimizer
* weight_decay
* num_train_epochs: defaults to 3.
* save_strategy: defaults to 'steps' (因此默认情况下，每 500 steps 保存一次)
  - no
  - epoch: at the end of each epoch
  - steps: for every `save_steps`
* save_steps: defaults to 500
* save_total_limit: deletes the older checkpoints in `output_dir`
* eval_steps: when eval_strategy is 'steps'
* load_best_model_at_end: 是否在训练结束后加载 best model
* metric_for_best_model:

* seed: random seed that will be set at the beginning of training, also consider `model_init`
* max_steps: override `num_train_epochs`
* lr_scheduler_type: defaults to `linear`
* dataloader_drop_last

* prediction_loss_only: for eval and generating preds
* gradient_accumulation_steps
* eval_accumulation_steps
* eval_delay
* adam_beta1
* adam_beta2
* adam_epsilon
* max_grad_norm
* run_name: typically used for `mlflow` or `wandb`




args = TrainingArguments(
    f"bert-finetuned-therapy-line-en",
    evaluation_strategy = "epoch",
    save_strategy = "epoch",
    learning_rate=1e-5,
    num_train_epochs=10,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model=metric_name,
    #push_to_hub=True,
)


args = TrainingArguments(
    f"{model_name}-finetuned-{task}",
    evaluation_strategy = "epoch",
    learning_rate=1e-5,
    num_train_epochs=6,
    weight_decay=0.01,
    push_to_hub=False,
)
