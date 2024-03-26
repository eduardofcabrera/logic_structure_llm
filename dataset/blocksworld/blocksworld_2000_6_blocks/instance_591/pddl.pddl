

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b e)
(ontable c)
(ontable d)
(on e d)
(clear a)
(clear b)
(clear c)
)
(:goal
(and
(on b d)
(on c e)
(on d a))
)
)


