

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b d)
(on c e)
(on d a)
(ontable e)
(clear b)
(clear c)
)
(:goal
(and
(on b e)
(on c b)
(on d a))
)
)


