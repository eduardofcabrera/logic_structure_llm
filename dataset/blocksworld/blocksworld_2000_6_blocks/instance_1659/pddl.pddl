

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b c)
(ontable c)
(ontable d)
(ontable e)
(clear a)
(clear b)
(clear d)
(clear e)
)
(:goal
(and
(on b d)
(on c e)
(on d a)
(on e b))
)
)


