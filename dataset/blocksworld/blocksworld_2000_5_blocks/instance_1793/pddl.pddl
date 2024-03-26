

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b c)
(on c e)
(on d a)
(ontable e)
(clear b)
(clear d)
)
(:goal
(and
(on d e))
)
)


